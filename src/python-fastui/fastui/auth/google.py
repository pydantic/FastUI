from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, AsyncIterator, Dict, List, Optional, Tuple, Union, cast
from urllib.parse import urlencode

import httpx
from pydantic import BaseModel, SecretStr, TypeAdapter

if TYPE_CHECKING:
    from fastapi import Request
    from fastapi.responses import JSONResponse


@dataclass
class GoogleExchangeError:
    error: str
    error_description: Union[str, None] = None


@dataclass
class GoogleExchange:
    access_token: str
    token_type: str
    scope: str
    expires_in: int
    refresh_token: Union[str, None] = None


google_exchange_type = TypeAdapter(Union[GoogleExchange, GoogleExchangeError])


class GoogleUser(BaseModel):
    id: str
    email: Optional[str] = None
    verified_email: Optional[bool] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None


class GoogleAuthProvider:
    def __init__(
        self,
        httpx_client: 'httpx.AsyncClient',
        google_client_id: str,
        google_client_secret: SecretStr,
        redirect_uri: Union[str, None] = None,
        scopes: Union[List[str], None] = None,
        state_provider: Union['StateProvider', bool] = True,
        exchange_cache_age: Union[timedelta, None] = timedelta(seconds=30),
    ):
        self._httpx_client = httpx_client
        self._google_client_id = google_client_id
        self._google_client_secret = google_client_secret
        self._redirect_uri = redirect_uri
        self._scopes = scopes or [
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
        ]
        self._state_provider = (
            state_provider if isinstance(state_provider, StateProvider) else StateProvider(google_client_secret)
        )
        self._exchange_cache_age = exchange_cache_age

    @classmethod
    @asynccontextmanager
    async def create(
        cls,
        client_id: str,
        client_secret: SecretStr,
        redirect_uri: Union[str, None] = None,
        state_provider: Union['StateProvider', bool] = True,
        exchange_cache_age: Union[timedelta, None] = timedelta(seconds=10),
    ) -> AsyncIterator['GoogleAuthProvider']:
        async with httpx.AsyncClient() as client:
            yield cls(
                client,
                client_id,
                client_secret,
                redirect_uri=redirect_uri,
                state_provider=state_provider,
                exchange_cache_age=exchange_cache_age,
            )

    async def authorization_url(self) -> str:
        params = {
            'client_id': self._google_client_id,
            'response_type': 'code',
            'scope': ' '.join(self._scopes),
            'redirect_uri': self._redirect_uri,
            'access_type': 'offline',
            'prompt': 'consent',
        }
        if self._state_provider:
            params['state'] = await self._state_provider.new_state()
        return f'https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}'

    async def exchange_code(self, code: str) -> GoogleExchange:
        if self._exchange_cache_age:
            cache_key = f'{code}'
            if exchange := EXCHANGE_CACHE.get(cache_key, self._exchange_cache_age):
                return exchange
            else:
                print('getting exchange code from google and setting cache')
                exchange = await self._exchange_code(code)
                EXCHANGE_CACHE.set(cache_key, exchange, self._exchange_cache_age)
                return exchange
        else:
            return await self._exchange_code(code)

    async def _exchange_code(self, code: str) -> GoogleExchange:
        params = {
            'client_id': self._google_client_id,
            'client_secret': self._google_client_secret.get_secret_value(),
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self._redirect_uri,
        }
        r = await self._httpx_client.post(
            'https://oauth2.googleapis.com/token',
            data=params,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
        )
        r.raise_for_status()
        exchange_response = google_exchange_type.validate_json(r.content)
        if isinstance(exchange_response, GoogleExchangeError):
            raise AuthError('Google OAuth error', code=exchange_response.error)
        else:
            return cast(GoogleExchange, exchange_response)

    async def refresh_access_token(self, refresh_token: str) -> GoogleExchange:
        params = {
            'client_id': self._google_client_id,
            'client_secret': self._google_client_secret.get_secret_value(),
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token',
        }
        response = await self._httpx_client.post(
            'https://oauth2.googleapis.com/token',
            data=params,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
        )
        response.raise_for_status()
        exchange_response = google_exchange_type.validate_json(response.content)
        if isinstance(exchange_response, GoogleExchangeError):
            raise AuthError('Google OAuth error', code=exchange_response.error)
        else:
            new_access_token = cast(GoogleExchange, exchange_response)
            return new_access_token

    async def get_google_user(self, exchange: GoogleExchange) -> GoogleUser:
        headers = {
            'Authorization': f'Bearer {exchange.access_token}',
            'Accept': 'application/json',
        }
        user_response = await self._httpx_client.get('https://www.googleapis.com/oauth2/v1/userinfo', headers=headers)
        user_response.raise_for_status()
        return GoogleUser.model_validate_json(user_response.content)


class ExchangeCache:
    def __init__(self):
        self._cache: Dict[str, Tuple[datetime, GoogleExchange]] = {}

    def get(self, key: str, max_age: timedelta) -> Union[GoogleExchange, None]:
        now = datetime.now()
        if (value := self._cache.get(key)) and now - value[0] <= max_age:
            return value[1]

    def set(self, key: str, value: GoogleExchange, max_age: timedelta) -> None:
        print('setting cache')
        self._cache[key] = (datetime.now(), value)
        print('cache', self._cache)

    def _purge(self, max_age: timedelta) -> None:
        now = datetime.now()
        self._cache = {key: value for key, value in self._cache.items() if now - value[0] <= max_age}


EXCHANGE_CACHE = ExchangeCache()


class AuthError(RuntimeError):
    def __init__(self, message: str, code: str):
        super().__init__(message)
        self.code = code

    @staticmethod
    def fastapi_handle(_request: 'Request', e: 'AuthError') -> 'JSONResponse':
        return JSONResponse({'detail': str(e)}, status_code=400)


class StateProvider:
    def __init__(self, secret: SecretStr, max_age: timedelta = timedelta(minutes=5)):
        self._secret = secret
        self._max_age = max_age

    async def new_state(self) -> str:
        import jwt

        data = {'created_at': datetime.now().isoformat()}
        return jwt.encode(data, self._secret.get_secret_value(), algorithm='HS256')

    async def check_state(self, state: str) -> bool:
        import jwt

        try:
            d = jwt.decode(state, self._secret.get_secret_value(), algorithms=['HS256'])
            created_at = datetime.fromisoformat(d['created_at'])
            return datetime.now() - created_at <= self._max_age
        except jwt.DecodeError:
            return False
