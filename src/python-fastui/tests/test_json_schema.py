from dirty_equals import IsPartialDict
from fastui import FastUI
from fastui.generate_typescript import generate_json_schema


async def test_json_schema():
    schema = generate_json_schema(FastUI)
    assert schema == {
        '$defs': IsPartialDict({'AnyEvent': IsPartialDict()}),
        'items': {'$ref': '#/$defs/FastProps'},
        'title': 'FastUI',
        'type': 'array',
    }
    # TODO test more specific cases
