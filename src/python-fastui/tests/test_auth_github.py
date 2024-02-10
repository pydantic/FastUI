from datetime import datetime
from typing import List, Optional

import httpx
import pytest
from fastapi import FastAPI
from fastui.auth import AuthError, GitHubAuthProvider, GitHubEmail
from fastui.auth.github import EXCHANGE_CACHE
from pydantic import SecretStr


@pytest.fixture
def github_requests() -> List[str]:
    return []


@pytest.fixture
def fake_github_app(github_requests: List[str]) -> FastAPI:
    app = FastAPI()

    @app.post('/login/oauth/access_token')
    async def access_token(code: str, client_id: str, client_secret: str, redirect_uri: Optional[str] = None):
        r = f'/login/oauth/access_token code={code}'
        if redirect_uri:
            r += f' redirect_uri={redirect_uri}'
        github_requests.append(r)
        assert client_id == '1234'
        assert client_secret == 'secret'
        if code == 'good_user':
            return {'access_token': 'good_token_user', 'token_type': 'bearer', 'scope': 'user'}
        elif code == 'good':
            return {'access_token': 'good_token', 'token_type': 'bearer', 'scope': ''}
        elif code == 'bad_expected':
            return {'error': 'bad_verification_code'}
        else:
            return {'error': 'bad_code'}

    @app.get('/user')
    async def user():
        github_requests.append('/user')
        return {
            'login': 'test_user',
            'name': 'Test User',
            'email': 'test@example.com',
            'avatar_url': 'https://example.com/avatar.png',
            'created_at': '2022-01-01T00:00:00Z',
            'updated_at': '2022-01-01T00:00:00Z',
            'public_repos': 0,
            'public_gists': 0,
            'followers': 0,
            'following': 0,
            'company': None,
            'blog': None,
            'location': None,
            'hireable': None,
            'bio': None,
        }

    @app.get('/user/emails')
    async def user_emails():
        github_requests.append('/user/emails')
        return [
            {'email': 'foo@example.com', 'primary': False, 'verified': True, 'visibility': None},
            {'email': 'bar@example.com', 'primary': True, 'verified': True, 'visibility': 'public'},
        ]

    return app


@pytest.fixture
async def httpx_client(fake_github_app: FastAPI):
    async with httpx.AsyncClient(app=fake_github_app) as client:
        yield client


@pytest.fixture
async def github_auth_provider(httpx_client: httpx.AsyncClient):
    return GitHubAuthProvider(
        httpx_client=httpx_client,
        github_client_id='1234',
        github_client_secret=SecretStr('secret'),
        state_provider=False,
        exchange_cache_age=None,
    )


async def test_get_auth_url(github_auth_provider: GitHubAuthProvider):
    url = await github_auth_provider.authorization_url()
    # no state here
    assert url == 'https://github.com/login/oauth/authorize?client_id=1234'


async def test_get_auth_url_scopes(httpx_client: httpx.AsyncClient):
    provider = GitHubAuthProvider(
        httpx_client=httpx_client,
        github_client_id='1234',
        github_client_secret=SecretStr('secret'),
        scopes=['user:email', 'read:org'],
        state_provider=False,
        exchange_cache_age=None,
    )
    url = await provider.authorization_url()
    # insert_assert(url)
    assert url == 'https://github.com/login/oauth/authorize?client_id=1234&scope=user%3Aemail+read%3Aorg'


async def test_exchange_ok(github_auth_provider: GitHubAuthProvider, github_requests: List[str]):
    assert github_requests == []
    exchange = await github_auth_provider.exchange_code('good')
    assert exchange.access_token == 'good_token'
    assert exchange.token_type == 'bearer'
    assert exchange.scope == []
    assert github_requests == ['/login/oauth/access_token code=good']


async def test_exchange_ok_user(github_auth_provider: GitHubAuthProvider):
    exchange = await github_auth_provider.exchange_code('good_user')
    assert exchange.access_token == 'good_token_user'
    assert exchange.token_type == 'bearer'
    assert exchange.scope == ['user']


async def test_exchange_bad_expected(github_auth_provider: GitHubAuthProvider):
    with pytest.raises(AuthError, match='^Invalid GitHub verification code'):
        await github_auth_provider.exchange_code('bad_expected')


async def test_exchange_bad_unexpected(github_auth_provider: GitHubAuthProvider):
    with pytest.raises(RuntimeError, match='^Unexpected response from GitHub access token exchange'):
        await github_auth_provider.exchange_code('unknown')


@pytest.fixture
async def github_auth_provider_state(fake_github_app: FastAPI, httpx_client: httpx.AsyncClient):
    return GitHubAuthProvider(
        httpx_client=httpx_client,
        github_client_id='1234',
        github_client_secret=SecretStr('secret'),
        state_provider=True,
    )


async def test_exchange_no_state(github_auth_provider_state: GitHubAuthProvider):
    with pytest.raises(AuthError, match='^Missing GitHub auth state'):
        await github_auth_provider_state.exchange_code('good')


async def test_exchange_bad_state(github_auth_provider_state: GitHubAuthProvider):
    with pytest.raises(AuthError, match='^Invalid GitHub auth state'):
        await github_auth_provider_state.exchange_code('good', 'bad_state')


async def test_exchange_good_state(github_auth_provider_state: GitHubAuthProvider):
    url = await github_auth_provider_state.authorization_url()
    assert url.startswith('https://github.com/login/oauth/authorize?client_id=1234&state=')
    state = url.rsplit('=', 1)[-1]

    exchange = await github_auth_provider_state.exchange_code('good', state)
    assert exchange.access_token == 'good_token'


async def test_exchange_bad_state_file_exists(github_auth_provider_state: GitHubAuthProvider):
    url = await github_auth_provider_state.authorization_url()
    assert url.startswith('https://github.com/login/oauth/authorize?client_id=1234&state=')

    with pytest.raises(AuthError, match='^Invalid GitHub auth state'):
        await github_auth_provider_state.exchange_code('good', 'bad_state')


async def test_exchange_ok_repeat(github_auth_provider: GitHubAuthProvider, github_requests: List[str]):
    assert github_requests == []
    exchange = await github_auth_provider.exchange_code('good')
    assert exchange.access_token == 'good_token'
    assert exchange.token_type == 'bearer'
    assert exchange.scope == []
    assert github_requests == ['/login/oauth/access_token code=good']

    exchange = await github_auth_provider.exchange_code('good')
    assert exchange.access_token == 'good_token'

    assert github_requests == ['/login/oauth/access_token code=good', '/login/oauth/access_token code=good']


async def test_exchange_ok_repeat_cached(
    fake_github_app: FastAPI, httpx_client: httpx.AsyncClient, github_requests: List[str]
):
    github_auth_provider = GitHubAuthProvider(
        httpx_client=httpx_client,
        github_client_id='1234',
        github_client_secret=SecretStr('secret'),
        state_provider=False,
    )
    EXCHANGE_CACHE.clear()
    assert len(EXCHANGE_CACHE) == 0
    assert github_requests == []
    await github_auth_provider.exchange_code('good')
    assert len(EXCHANGE_CACHE) == 1
    assert github_requests == ['/login/oauth/access_token code=good']
    await github_auth_provider.exchange_code('good')
    assert github_requests == ['/login/oauth/access_token code=good']  # no repeat request to github
    await github_auth_provider.exchange_code('good_user')
    assert github_requests == ['/login/oauth/access_token code=good', '/login/oauth/access_token code=good_user']


async def test_exchange_cached_purge(fake_github_app: FastAPI, httpx_client: httpx.AsyncClient):
    github_auth_provider = GitHubAuthProvider(
        httpx_client=httpx_client,
        github_client_id='1234',
        github_client_secret=SecretStr('secret'),
        state_provider=False,
    )
    EXCHANGE_CACHE.clear()
    await github_auth_provider.exchange_code('good')
    assert len(EXCHANGE_CACHE) == 1

    # manually add an old entry
    EXCHANGE_CACHE._data['old'] = (datetime(2020, 1, 1), 'old_token')
    assert len(EXCHANGE_CACHE) == 2

    await github_auth_provider.exchange_code('good')
    assert len(EXCHANGE_CACHE) == 1


async def test_exchange_redirect_url(
    fake_github_app: FastAPI, httpx_client: httpx.AsyncClient, github_requests: List[str]
):
    github_auth_provider = GitHubAuthProvider(
        httpx_client=httpx_client,
        github_client_id='1234',
        github_client_secret=SecretStr('secret'),
        redirect_uri='/callback',
        state_provider=False,
        exchange_cache_age=None,
    )
    url = await github_auth_provider.authorization_url()
    assert url == 'https://github.com/login/oauth/authorize?client_id=1234&redirect_uri=%2Fcallback'
    exchange = await github_auth_provider.exchange_code('good')
    assert exchange.access_token == 'good_token'
    assert github_requests == ['/login/oauth/access_token code=good redirect_uri=/callback']


async def test_get_github_user(github_auth_provider: GitHubAuthProvider, github_requests: List[str]):
    assert github_requests == []
    exchange = await github_auth_provider.exchange_code('good')
    assert github_requests == ['/login/oauth/access_token code=good']
    user = await github_auth_provider.get_github_user(exchange)
    assert user.login == 'test_user'
    assert user.name == 'Test User'
    assert user.email == 'test@example.com'

    assert github_requests == ['/login/oauth/access_token code=good', '/user']


async def test_get_github_user_emails(github_auth_provider: GitHubAuthProvider, github_requests: List[str]):
    assert github_requests == []
    exchange = await github_auth_provider.exchange_code('good')
    assert github_requests == ['/login/oauth/access_token code=good']
    emails = await github_auth_provider.get_github_user_emails(exchange)
    assert emails == [
        GitHubEmail(email='foo@example.com', primary=False, verified=True, visibility=None),
        GitHubEmail(email='bar@example.com', primary=True, verified=True, visibility='public'),
    ]
    assert github_requests == ['/login/oauth/access_token code=good', '/user/emails']


async def test_create():
    async with GitHubAuthProvider.create('foo', SecretStr('bar')) as provider:
        assert isinstance(provider._httpx_client, httpx.AsyncClient)
