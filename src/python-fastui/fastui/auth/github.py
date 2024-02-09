import secrets
import tempfile
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, AsyncIterator, Dict, List, Union, cast
from urllib.parse import urlencode

import httpx
from pydantic import BaseModel, SecretStr, TypeAdapter, field_validator

if TYPE_CHECKING:
    from fastapi import Request
    from fastapi.responses import JSONResponse


@dataclass
class GitHubExchangeError:
    error: str
    error_description: Union[str, None] = None


@dataclass
class GitHubExchange:
    access_token: str
    token_type: str
    scope: List[str]

    @field_validator('scope', mode='before')
    def check_scope(cls, v: str) -> List[str]:
        return [s for s in v.split(',') if s]


github_exchange_type = TypeAdapter(Union[GitHubExchange, GitHubExchangeError])


class GithubUser(BaseModel):
    login: str
    name: Union[str, None]
    email: Union[str, None]
    avatar_url: str
    created_at: datetime
    updated_at: datetime
    public_repos: int
    public_gists: int
    followers: int
    following: int
    company: Union[str, None]
    blog: Union[str, None]
    location: Union[str, None]
    hireable: Union[bool, None]
    bio: Union[str, None]
    twitter_username: Union[str, None] = None


class GitHubEmail(BaseModel):
    email: str
    primary: bool
    verified: bool
    visibility: Union[str, None]


github_emails_ta = TypeAdapter(List[GitHubEmail])


class GitHubAuthProvider:
    """
    For details see https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps.
    """

    def __init__(
        self,
        httpx_client: httpx.AsyncClient,
        github_client_id: str,
        github_client_secret: SecretStr,
        *,
        redirect_uri: Union[str, None] = None,
        state_provider: Union['AbstractStateProvider', bool] = True,
        exchange_cache_age: Union[timedelta, None] = timedelta(seconds=10),
    ):
        self._httpx_client = httpx_client
        self._github_client_id = github_client_id
        self._github_client_secret = github_client_secret
        self._redirect_uri = redirect_uri
        if state_provider is True:
            self._state_provider = _get_default_state_provider()
        elif state_provider is False:
            self._state_provider = None
        else:
            self._state_provider = state_provider
        # cache exchange responses, see `exchange_code` for details
        self._exchange_cache_age = exchange_cache_age
        self._exchange_cache: dict[str, tuple[datetime, GitHubExchange]] = {}

    @classmethod
    @asynccontextmanager
    async def create(
        cls,
        client_id: str,
        client_secret: SecretStr,
        *,
        redirect_uri: Union[str, None] = None,
        state_provider: Union['AbstractStateProvider', bool] = True,
        exchange_cache_age: Union[timedelta, None] = timedelta(seconds=10),
    ) -> AsyncIterator['GitHubAuthProvider']:
        """
        Async context manager to create a GitHubAuth instance with a new `httpx.AsyncClient`.
        """
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
        params = {'client_id': self._github_client_id}
        if self._redirect_uri:
            params['redirect_uri'] = self._redirect_uri
        if self._state_provider:
            params['state'] = await self._state_provider.create_store_state()
        return f'https://github.com/login/oauth/authorize?{urlencode(params)}'

    async def exchange_code(self, code: str, state: Union[str, None] = None) -> GitHubExchange:
        """
        Exchange a code for an access token.

        If `self._exchange_cache_age` is not `None` (the default), responses are cached for the given duration, to
        work around issues with React often sending the same request multiple times in development mode.
        """
        if self._exchange_cache_age:
            cache_key = f'{code}:{state}'
            now = datetime.now()
            min_timestamp = now - self._exchange_cache_age
            # remove anything older than the cache age
            self._exchange_cache = {k: v for k, v in self._exchange_cache.items() if v[0] > min_timestamp}

            if cache_value := self._exchange_cache.get(cache_key):
                return cache_value[1]
            else:
                exchange = await self._exchange_code(code, state)
                self._exchange_cache[cache_key] = (now, exchange)
                return exchange
        else:
            return await self._exchange_code(code, state)

    async def _exchange_code(self, code: str, state: Union[str, None] = None) -> GitHubExchange:
        if self._state_provider:
            if state is None:
                raise AuthError('Missing GitHub auth state', code='missing_state')
            elif not await self._state_provider.check_state(state):
                raise AuthError('Invalid GitHub auth state', code='invalid_state')

        params = {
            'client_id': self._github_client_id,
            'client_secret': self._github_client_secret.get_secret_value(),
            'code': code,
        }
        if self._redirect_uri:
            params['redirect_uri'] = self._redirect_uri

        r = await self._httpx_client.post(
            'https://github.com/login/oauth/access_token',
            params=params,
            headers={'Accept': 'application/json'},
        )
        r.raise_for_status()
        exchange_response = github_exchange_type.validate_json(r.content)
        if isinstance(exchange_response, GitHubExchangeError):
            if exchange_response.error == 'bad_verification_code':
                raise AuthError('Invalid GitHub verification code', code=exchange_response.error)
            else:
                raise RuntimeError(f'Unexpected response from GitHub access token exchange: {r.text}')
        else:
            return cast(GitHubExchange, exchange_response)

    async def get_github_user(self, exchange: GitHubExchange) -> GithubUser:
        """
        See https://docs.github.com/en/rest/users/users#get-the-authenticated-user
        """
        headers = self._auth_headers(exchange)
        user_response = await self._httpx_client.get('https://api.github.com/user', headers=headers)
        user_response.raise_for_status()
        return GithubUser.model_validate_json(user_response.content)

    async def get_github_user_emails(self, exchange: GitHubExchange) -> List[GitHubEmail]:
        """
        See https://docs.github.com/en/rest/users/emails
        """
        headers = self._auth_headers(exchange)
        emails_response = await self._httpx_client.get('https://api.github.com/user/emails', headers=headers)
        emails_response.raise_for_status()
        return github_emails_ta.validate_json(emails_response.content)

    @staticmethod
    def _auth_headers(exchange: GitHubExchange) -> Dict[str, str]:
        return {
            'Authorization': f'Bearer {exchange.access_token}',
            'Accept': 'application/vnd.github+json',
        }


class AuthError(RuntimeError):
    # TODO if we add other providers, this should become shared

    def __init__(self, message: str, *, code: str):
        super().__init__(message)
        self.code = code

    @staticmethod
    def fastapi_handle(_request: 'Request', e: 'AuthError') -> 'JSONResponse':
        from fastapi.responses import JSONResponse

        return JSONResponse({'detail': str(e)}, status_code=400)


class AbstractStateProvider(ABC):
    """
    This class is used to store and validate the state parameter used in the GitHub OAuth flow.

    You can override this class to implement a persistent state provider.
    """

    # TODO if we add other providers, this might become shared?

    async def create_store_state(self) -> str:
        state = secrets.token_urlsafe()
        await self.store_state(state)
        return state

    @abstractmethod
    async def store_state(self, state: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def check_state(self, state: str) -> bool:
        raise NotImplementedError


class TmpFileStateProvider(AbstractStateProvider):
    """
    This is a simple state provider for the GitHub OAuth flow which uses a file in the system's temporary directory.
    """

    def __init__(self, path: Union[Path, None] = None):
        self._path = path or Path(tempfile.gettempdir()) / 'fastui_github_auth_states.txt'

    async def store_state(self, state: str) -> None:
        with self._path.open('a') as f:
            f.write(f'{state}\n')

    async def check_state(self, state: str) -> bool:
        if not self._path.exists():
            return False

        remaining_lines = []
        found = False
        for line in self._path.read_text().splitlines():
            if line == state:
                found = True
            else:
                remaining_lines.append(line)

        if found:
            self._path.write_text('\n'.join(remaining_lines) + '\n')
        return found


# we have a global so creating new instances of the auth object will reuse the same state provider
_DEFAULT_STATE_PROVIDER: Union[AbstractStateProvider, None] = None


def _get_default_state_provider() -> AbstractStateProvider:
    global _DEFAULT_STATE_PROVIDER
    if _DEFAULT_STATE_PROVIDER is None:
        _DEFAULT_STATE_PROVIDER = TmpFileStateProvider()
    return _DEFAULT_STATE_PROVIDER