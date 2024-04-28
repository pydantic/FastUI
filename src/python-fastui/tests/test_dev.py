from unittest.mock import patch

from httpx import AsyncClient

from fastui.dev import dev_fastapi_app


def mock_signal(_sig, on_signal):
    on_signal()


async def test_dev_connect():
    with patch('fastui.dev.signal.signal', new=mock_signal):
        app = dev_fastapi_app()
        async with app.router.lifespan_context(app):
            async with AsyncClient(app=app, base_url='http://test') as client:
                r = await client.get('/api/__dev__/reload')
                assert r.status_code == 200
                assert r.headers['content-type'] == 'text/plain; charset=utf-8'
                assert r.text.startswith('fastui-dev-reload\n')
