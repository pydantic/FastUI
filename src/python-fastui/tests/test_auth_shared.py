import pytest
from fastapi import FastAPI
from fastui.auth import AuthError, AuthRedirect, fastapi_auth_exception_handling
from starlette.testclient import TestClient


@pytest.fixture(name='app')
def app_fixture() -> FastAPI:
    app = FastAPI()
    fastapi_auth_exception_handling(app)

    @app.post('/do-redirect/')
    async def do_redirect():
        raise AuthRedirect('/new-path')

    @app.post('/do-error/')
    async def do_error():
        raise AuthError('error message', code='error-code')

    return app


@pytest.fixture
def client(app: FastAPI):
    with TestClient(app) as test_client:
        yield test_client


def test_auth_redirect(client: TestClient):
    r = client.post('/do-redirect/')
    assert r.status_code == 345
    # insert_assert(r.json())
    assert r.json() == [{'event': {'url': '/new-path', 'type': 'go-to'}, 'type': 'FireEvent'}]


def test_auth_error(client: TestClient):
    r = client.post('/do-error/')
    assert r.status_code == 401
    assert r.json() == {'detail': 'error message'}
