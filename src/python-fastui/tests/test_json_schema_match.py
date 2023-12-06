import json
import typing
from pathlib import Path

import pytest
from fastui import AnyComponent
from pydantic import TypeAdapter

THIS_DIR = Path(__file__).parent
with (THIS_DIR / 'react-fastui-json-schema.json').open('rb') as npm_file:
    REACT_SCHEMA_DEFS = json.load(npm_file)['definitions']

ta = TypeAdapter(AnyComponent)
json_schema = ta.json_schema(by_alias=True, mode='serialization', ref_template='#/definitions/{model}')
components_union = json_schema['oneOf']
components_union_set = set(d['$ref'] for d in components_union)


def python_model_iter():
    python_defs = json_schema['$defs']
    for d in components_union:
        key = d['$ref'].split('/')[-1]
        yield pytest.param(python_defs[key], id=key)


def fix_pydantic_schema(s: typing.Any):
    """
    * convert pydantic's `anyOf` all components to typescripts `'$ref': '#/definitions/FastProps'`
    * switch "type": "integer" to "type": "number"
    * switch `{"anyOf": [{"type": "XXX"}, {"type": "null"}]}` to `{"type": "XXX"}`
    * switch `{"oneOf": ..., "discriminator": ...}` to `{"anyOf": ...}`
    """
    if isinstance(s, dict):
        for k, v in s.items():
            if k == 'type' and v == 'integer':
                s[k] = 'number'
            if isinstance(v, dict):
                if any_of := v.get('anyOf'):
                    refs = [d.get('$ref') for d in any_of]
                    if set(refs) == components_union_set:
                        v.pop('anyOf')
                        v['$ref'] = '#/definitions/FastProps'
                        continue

                    null_type = {'type': 'null'}
                    if null_type in any_of and len(any_of) == 2:
                        other = next(d for d in any_of if d != null_type)
                        v.clear()
                        v.update(other)

                if 'discriminator' in v and (one_of := v.get('oneOf')):
                    v.clear()
                    v['anyOf'] = one_of

            fix_pydantic_schema(v)
    elif isinstance(s, list):
        for item in s:
            fix_pydantic_schema(item)


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

    fix_pydantic_schema(model_properties)

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
