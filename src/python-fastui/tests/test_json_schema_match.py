import json
import typing
from pathlib import Path

import pytest
from fastui import AnyComponent
from pydantic import TypeAdapter

THIS_DIR = Path(__file__).parent
with (THIS_DIR / 'react-fastui-json-schema.json').open('rb') as npm_file:
    REACT_SCHEMA_DEFS = json.load(npm_file)['definitions']


def python_model_iter():
    ta = TypeAdapter(AnyComponent)
    json_schema = ta.json_schema(by_alias=True, mode='serialization')
    defs = json_schema['$defs']
    for d in json_schema['oneOf']:
        key = d['$ref'].split('/')[-1]
        yield pytest.param(defs[key], id=key)


@pytest.mark.parametrize('model_schema', python_model_iter())
def test_components_match(model_schema: typing.Dict[str, typing.Any]):
    title = model_schema.get('title')
    if title is None:
        all_of = model_schema['allOf']
        assert len(all_of) == 1
        ref = all_of[0]['$ref']
        title = ref.split('/')[-1]
        model_schema = model_schema['$defs'][title]

    react_title = f'{title}Props'

    try:
        react_schema = REACT_SCHEMA_DEFS[react_title]
    except KeyError as e:
        pytest.fail(f'No react model found with name {e}')

    model_properties = model_schema['properties']
    for value in model_properties.values():
        value.pop('title', None)
        value.pop('default', None)

    react_properties = react_schema['properties']
    # typescript-json-schema adds type to `const` properties while pydantic does not,
    # pydantic matches the example from JSON Schema's docs
    # https://json-schema.org/understanding-json-schema/reference/const
    react_properties['type'].pop('type')

    if 'className' in model_properties and 'className' in react_properties:
        # class name doesn't match due to recursive type
        model_properties.pop('className')
        react_properties.pop('className')

    # debug(model_properties, react_properties)
    assert model_properties == react_properties
