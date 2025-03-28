from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import timedelta
from typing import AsyncIterator, List, Optional, Union, cast
from urllib.parse import urlencode

import httpx
from pydantic import BaseModel, SecretStr, TypeAdapter

from .shared import AuthError, ExchangeCache, ExchangeData


@dataclass
class GoogleExchangeError:
    error: str
    error_description: Union[str, None] = None


@dataclass
class GoogleExchange(ExchangeData):
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
        self._exchange_cache_age = exchange_cache_age

    @classmethod
    @asynccontextmanager
    async def create(
        cls,
        client_id: str,
        client_secret: SecretStr,
        redirect_uri: Union[str, None] = None,
        exchange_cache_age: Union[timedelta, None] = timedelta(seconds=10),
    ) -> AsyncIterator['GoogleAuthProvider']:
        async with httpx.AsyncClient() as client:
            yield cls(
                client,
                client_id,
                client_secret,
                redirect_uri=redirect_uri,
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
        return f'https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}'

    async def exchange_code(self, code: str) -> GoogleExchange:
        if self._exchange_cache_age:
            cache_key = f'{code}'
            if exchange := EXCHANGE_CACHE.get(cache_key, self._exchange_cache_age):
                return exchange
            else:
                exchange = await self._exchange_code(code)
                EXCHANGE_CACHE.set(key=cache_key, value=exchange)
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


EXCHANGE_CACHE = ExchangeCache()
