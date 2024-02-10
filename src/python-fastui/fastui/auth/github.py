from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, AsyncIterator, Dict, List, Tuple, Union, cast
from urllib.parse import urlencode

from pydantic import BaseModel, SecretStr, TypeAdapter, field_validator

from .shared import AuthError

if TYPE_CHECKING:
    import httpx


__all__ = 'GitHubAuthProvider', 'GitHubExchange', 'GithubUser', 'GitHubEmail'


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
        httpx_client: 'httpx.AsyncClient',
        github_client_id: str,
        github_client_secret: SecretStr,
        *,
        redirect_uri: Union[str, None] = None,
        scopes: Union[List[str], None] = None,
        state_provider: Union['StateProvider', bool] = True,
        exchange_cache_age: Union[timedelta, None] = timedelta(seconds=30),
    ):
        """
        Arguments:
            httpx_client: An instance of `httpx.AsyncClient` to use for making requests to GitHub.
            github_client_id: The client ID of the GitHub OAuth app.
            github_client_secret: The client secret of the GitHub OAuth app.
            redirect_uri: The URL in your app where users will be sent after authorization, if custom
            scopes: See https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps#available-scopes
            state_provider: If `True`, use a `StateProvider` to generate and validate state parameters for the OAuth
                flow, you can also provide an instance directly.
            exchange_cache_age: If not `None`,
                responses from the access token exchange are cached for the given duration.
        """
        self._httpx_client = httpx_client
        self._github_client_id = github_client_id
        self._github_client_secret = github_client_secret
        self._redirect_uri = redirect_uri
        self._scopes = scopes
        if state_provider is True:
            self._state_provider = StateProvider(github_client_secret)
        elif state_provider is False:
            self._state_provider = None
        else:
            self._state_provider = state_provider
        # cache exchange responses, see `exchange_code` for details
        self._exchange_cache_age = exchange_cache_age

    @classmethod
    @asynccontextmanager
    async def create(
        cls,
        client_id: str,
        client_secret: SecretStr,
        *,
        redirect_uri: Union[str, None] = None,
        state_provider: Union['StateProvider', bool] = True,
        exchange_cache_age: Union[timedelta, None] = timedelta(seconds=10),
    ) -> AsyncIterator['GitHubAuthProvider']:
        """
        Async context manager to create a GitHubAuth instance with a new `httpx.AsyncClient`.
        """
        import httpx

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
        """
        See https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps#1-request-a-users-github-identity
        """
        params = {'client_id': self._github_client_id}
        if self._redirect_uri:
            params['redirect_uri'] = self._redirect_uri
        if self._scopes:
            params['scope'] = ' '.join(self._scopes)
        if self._state_provider:
            params['state'] = await self._state_provider.new_state()
        return f'https://github.com/login/oauth/authorize?{urlencode(params)}'

    async def exchange_code(self, code: str, state: Union[str, None] = None) -> GitHubExchange:
        """
        Exchange a code for an access token.

        If `self._exchange_cache_age` is not `None` (the default), responses are cached for the given duration to
        work around issues with React often sending the same request multiple times in development mode.
        """
        if self._exchange_cache_age:
            cache_key = f'{code}:{state}'
            if exchange := EXCHANGE_CACHE.get(cache_key, self._exchange_cache_age):
                return exchange
            else:
                exchange = await self._exchange_code(code, state)
                EXCHANGE_CACHE.set(cache_key, exchange)
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


class ExchangeCache:
    def __init__(self):
        self._data: Dict[str, Tuple[datetime, GitHubExchange]] = {}

    def get(self, key: str, max_age: timedelta) -> Union[GitHubExchange, None]:
        self._purge(max_age)
        if v := self._data.get(key):
            return v[1]

    def set(self, key: str, value: GitHubExchange) -> None:
        self._data[key] = (datetime.now(), value)

    def _purge(self, max_age: timedelta) -> None:
        """
        Remove old items from the exchange cache
        """
        min_timestamp = datetime.now() - max_age
        to_remove = [k for k, (ts, _) in self._data.items() if ts < min_timestamp]
        for k in to_remove:
            del self._data[k]

    def __len__(self) -> int:
        return len(self._data)

    def clear(self) -> None:
        self._data.clear()


# exchange cache is a singleton so instantiating a new GitHubAuthProvider reuse the same cache
EXCHANGE_CACHE = ExchangeCache()


class StateProvider:
    """
    This is a simple state provider for the GitHub OAuth flow which uses a JWT to create an unguessable "state" string.

    Requires `PyJWT` to be installed.
    """

    def __init__(self, secret: SecretStr, max_age: timedelta = timedelta(minutes=5)):
        self._secret = secret
        self._max_age = max_age

    async def new_state(self) -> str:
        import jwt

        data = {'exp': datetime.now(tz=timezone.utc) + self._max_age}
        return jwt.encode(data, self._secret.get_secret_value(), algorithm='HS256')

    async def check_state(self, state: str) -> bool:
        import jwt

        try:
            jwt.decode(state, self._secret.get_secret_value(), algorithms=['HS256'])
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return False
        else:
            return True
