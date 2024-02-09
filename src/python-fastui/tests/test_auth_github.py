from pathlib import Path

import httpx
import pytest
from fastapi import FastAPI
from fastui.auth import AuthError, GitHubAuthProvider
from fastui.auth.github import TmpFileStateProvider
from pydantic import SecretStr


@pytest.fixture
def github_requests() -> list[str]:
    return []


@pytest.fixture
def fake_github_app(github_requests: list[str]) -> FastAPI:
    app = FastAPI()

    @app.post('/login/oauth/access_token')
    async def access_token(code: str, client_id: str, client_secret: str):
        github_requests.append(f'/login/oauth/access_token code={code}')
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

    return app


@pytest.fixture
async def github_auth_provider(fake_github_app: FastAPI):
    async with httpx.AsyncClient(app=fake_github_app) as client:
        yield GitHubAuthProvider(
            httpx_client=client,
            github_client_id='1234',
            github_client_secret=SecretStr('secret'),
            state_provider=False,
            exchange_cache_age=None,
        )


async def test_get_auth_url(github_auth_provider: GitHubAuthProvider):
    url = await github_auth_provider.authorization_url()
    # no state here
    assert url == 'https://github.com/login/oauth/authorize?client_id=1234'


async def test_exchange_ok(github_auth_provider: GitHubAuthProvider, github_requests: list[str]):
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
async def github_auth_provider_state(fake_github_app: FastAPI, tmp_path: Path):
    async with httpx.AsyncClient(app=fake_github_app) as client:
        yield GitHubAuthProvider(
            httpx_client=client,
            github_client_id='1234',
            github_client_secret=SecretStr('secret'),
            state_provider=TmpFileStateProvider(tmp_path / 'github_state.txt'),
        )


async def test_exchange_no_state(github_auth_provider_state: GitHubAuthProvider):
    with pytest.raises(AuthError, match='^Missing GitHub auth state'):
        await github_auth_provider_state.exchange_code('good')


async def test_exchange_bad_state(github_auth_provider_state: GitHubAuthProvider):
    with pytest.raises(AuthError, match='^Invalid GitHub auth state'):
        await github_auth_provider_state.exchange_code('good', 'bad_state')


async def test_exchange_good_state(github_auth_provider_state: GitHubAuthProvider, tmp_path: Path):
    url = await github_auth_provider_state.authorization_url()
    assert url.startswith('https://github.com/login/oauth/authorize?client_id=1234&state=')
    state = url.rsplit('=', 1)[-1]

    state_path = tmp_path / 'github_state.txt'
    assert state_path.read_text() == f'{state}\n'

    exchange = await github_auth_provider_state.exchange_code('good', state)
    assert exchange.access_token == 'good_token'

    # state should be cleared
    assert state_path.read_text() == '\n'


async def test_exchange_bad_state_file_exists(github_auth_provider_state: GitHubAuthProvider, tmp_path: Path):
    url = await github_auth_provider_state.authorization_url()
    assert url.startswith('https://github.com/login/oauth/authorize?client_id=1234&state=')
    state = url.rsplit('=', 1)[-1]

    state_path = tmp_path / 'github_state.txt'
    assert state_path.read_text() == f'{state}\n'

    with pytest.raises(AuthError, match='^Invalid GitHub auth state'):
        await github_auth_provider_state.exchange_code('good', 'bad_state')

    # state still there
    assert state_path.read_text() == f'{state}\n'


async def test_exchange_ok_repeat(github_auth_provider: GitHubAuthProvider, github_requests: list[str]):
    assert github_requests == []
    exchange = await github_auth_provider.exchange_code('good')
    assert exchange.access_token == 'good_token'
    assert exchange.token_type == 'bearer'
    assert exchange.scope == []
    assert github_requests == ['/login/oauth/access_token code=good']

    exchange = await github_auth_provider.exchange_code('good')
    assert exchange.access_token == 'good_token'

    assert github_requests == ['/login/oauth/access_token code=good', '/login/oauth/access_token code=good']


async def test_exchange_ok_repeat_cached(fake_github_app: FastAPI, github_requests: list[str]):
    async with httpx.AsyncClient(app=fake_github_app) as client:
        github_auth_provider = GitHubAuthProvider(
            httpx_client=client,
            github_client_id='1234',
            github_client_secret=SecretStr('secret'),
            state_provider=False,
        )
        assert github_requests == []
        await github_auth_provider.exchange_code('good')
        assert github_requests == ['/login/oauth/access_token code=good']
        await github_auth_provider.exchange_code('good')
        assert github_requests == ['/login/oauth/access_token code=good']  # no repeat request to github
        await github_auth_provider.exchange_code('good_user')
        assert github_requests == ['/login/oauth/access_token code=good', '/login/oauth/access_token code=good_user']


async def test_get_github_user(github_auth_provider: GitHubAuthProvider, github_requests: list[str]):
    assert github_requests == []
    exchange = await github_auth_provider.exchange_code('good')
    assert github_requests == ['/login/oauth/access_token code=good']
    user = await github_auth_provider.get_github_user(exchange)
    assert user.login == 'test_user'
    assert user.name == 'Test User'
    assert user.email == 'test@example.com'

    assert github_requests == ['/login/oauth/access_token code=good', '/user']
