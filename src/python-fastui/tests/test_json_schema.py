from dirty_equals import IsPartialDict
from fastapi import FastAPI
from fastui import FastUI, components
from fastui.generate_typescript import generate_json_schema
from httpx import AsyncClient


async def test_json_schema():
    schema = generate_json_schema(FastUI)
    assert schema == {
        '$defs': IsPartialDict({'AnyEvent': IsPartialDict()}),
        'items': {'$ref': '#/$defs/FastProps'},
        'title': 'FastUI',
        'type': 'array',
    }
    # TODO test more specific cases


async def test_openapi():
    app = FastAPI()

    @app.get('/api/', response_model=FastUI, response_model_exclude_none=True)
    def test_endpoint():
        return [components.Text(text='hello')]

    async with AsyncClient(app=app, base_url='http://test') as client:
        r = await client.get('/openapi.json')
        assert r.status_code == 200
        assert r.headers['content-type'] == 'application/json'
        assert r.json() == {
            'openapi': '3.1.0',
            'info': {
                'title': 'FastAPI',
                'version': '0.1.0',
            },
            'paths': IsPartialDict(),
            'components': IsPartialDict(),
        }
