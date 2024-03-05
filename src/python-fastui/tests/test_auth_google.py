from datetime import timedelta

import httpx
import pytest
from fastui.auth.google import (
    EXCHANGE_CACHE,
    AuthError,
    GoogleAuthProvider,
    GoogleExchange,
    GoogleUser,
)
from httpx import Request, Response
from pydantic import SecretStr


class MockTransport(httpx.AsyncBaseTransport):
    async def handle_async_request(self, request: Request) -> Response:
        url = str(request.url)
        method = request.method

        if url == 'https://oauth2.googleapis.com/token' and method == 'POST':
            print(request.read())
            if b'code=bad_code' in request.read():
                return Response(200, json={'error': 'bad code'})

            json_data = {
                'access_token': 'test_access_token',
                'token_type': 'Bearer',
                'expires_in': 3600,
                'refresh_token': 'test_refresh_token',
                'scope': 'email profile',
            }
            return Response(200, json=json_data)

        elif url == 'https://www.googleapis.com/oauth2/v1/userinfo' and method == 'GET':
            json_data = {
                'id': '12345',
                'email': 'user@example.com',
                'verified_email': True,
                'name': 'Test User',
                'given_name': 'Test',
                'family_name': 'User',
                'picture': 'https://example.com/avatar.png',
                'locale': 'en',
            }
            return Response(200, json=json_data)

        return Response(404, json={'error': 'not found'})


@pytest.fixture
async def mock_httpx_client() -> httpx.AsyncClient:
    client = httpx.AsyncClient(transport=MockTransport())
    yield client
    await client.aclose()


@pytest.fixture
async def google_auth_provider(mock_httpx_client: httpx.AsyncClient):
    return GoogleAuthProvider(
        httpx_client=mock_httpx_client,
        google_client_id='google_client_id',
        google_client_secret=SecretStr('google_client_secret'),
        redirect_uri='https://example.com/callback',
        scopes=['email', 'profile'],
        exchange_cache_age=timedelta(minutes=5),
    )


async def test_create():
    async with GoogleAuthProvider.create('foo', SecretStr('bar')) as provider:
        assert isinstance(provider._httpx_client, httpx.AsyncClient)


async def test_authorization_url(google_auth_provider: GoogleAuthProvider):
    url = await google_auth_provider.authorization_url()
    assert url.startswith('https://accounts.google.com/o/oauth2/v2/auth?')


async def test_exchange_code_success(google_auth_provider: GoogleAuthProvider):
    exchange = await google_auth_provider.exchange_code('good_code')
    assert isinstance(exchange, GoogleExchange)
    assert exchange.access_token == 'test_access_token'
    assert exchange.token_type == 'Bearer'
    assert exchange.scope == 'email profile'
    assert exchange.refresh_token == 'test_refresh_token'


async def test_exchange_code_error(google_auth_provider: GoogleAuthProvider):
    with pytest.raises(AuthError):
        await google_auth_provider.exchange_code('bad_code')


async def test_refresh_access_token(google_auth_provider: GoogleAuthProvider):
    new_token = await google_auth_provider.refresh_access_token('good_refresh_token')
    assert isinstance(new_token, GoogleExchange)
    assert new_token.access_token == 'test_access_token'


async def test_get_google_user(google_auth_provider: GoogleAuthProvider):
    exchange = GoogleExchange(
        access_token='good_access_token',
        token_type='Bearer',
        scope='email profile',
        expires_in=3600,
        refresh_token='good_refresh_token',
    )
    user = await google_auth_provider.get_google_user(exchange)
    assert isinstance(user, GoogleUser)
    assert user.id == '12345'
    assert user.email == 'user@example.com'


async def test_exchange_cache(
    google_auth_provider: GoogleAuthProvider,
):
    EXCHANGE_CACHE.clear()
    assert len(EXCHANGE_CACHE) == 0
    await google_auth_provider.exchange_code('good_code')
    assert len(EXCHANGE_CACHE) == 1
    await google_auth_provider.exchange_code('good_code')
    assert len(EXCHANGE_CACHE) == 1


async def test_exchange_no_cache(mock_httpx_client):
    EXCHANGE_CACHE.clear()
    provider = GoogleAuthProvider(
        httpx_client=mock_httpx_client,
        google_client_id='google_client_id',
        google_client_secret=SecretStr('google_client_secret'),
        redirect_uri='https://example.com/callback',
        scopes=['email', 'profile'],
        exchange_cache_age=None,
    )
    await provider.exchange_code('good_code')
    assert len(EXCHANGE_CACHE) == 0
    await provider.exchange_code('good_code')
    assert len(EXCHANGE_CACHE) == 0
