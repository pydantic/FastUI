import json
import typing
from pathlib import Path

import pytest
from dirty_equals import IsList
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


NULL_TYPE = {'type': 'null'}


def any_of_simple(any_of: typing.List[typing.Any]) -> typing.Union[typing.List[typing.Any], None]:
    new_types = []
    simple = True
    for s in any_of:
        if s == NULL_TYPE:
            continue
        elif len(s) == 1 and (value := s.get('type')):
            new_types.append(value)
        else:
            simple = False

    if simple:
        return new_types


def fix_pydantic_schema(s: typing.Any) -> None:
    """
    Convert pydantic JSON schema to match `typescript-json-schema`.
    """
    if isinstance(s, dict):
        s.pop('readOnly', None)

        if len(s) == 2 and 'discriminator' in s and (one_of := s.get('oneOf')):
            s.clear()
            s['anyOf'] = one_of
        else:
            for k, v in list(s.items()):
                if k == '$ref':
                    if v in {'#/definitions/DisplayLookup', '#/definitions/Link'}:
                        s['$ref'] = f'{v}Props'
                    elif v == '#/definitions/BaseModel':
                        s['$ref'] = '#/definitions/ModelData'
                    elif v == '#/definitions/DisplayMode':
                        display_mode = json_schema['$defs']['DisplayMode']
                        s.clear()
                        s.update(
                            enum=IsList(*display_mode['enum'], check_order=False),
                            type='string',
                        )
                    continue

                if isinstance(v, dict):
                    if any_of := v.get('anyOf'):
                        refs = [d.get('$ref') for d in any_of]
                        if set(refs) == components_union_set:
                            v.pop('anyOf')
                            v['$ref'] = '#/definitions/FastProps'
                            continue

                        if NULL_TYPE in any_of and len(any_of) == 2:
                            other = next(d for d in any_of if d != NULL_TYPE)
                            fix_pydantic_schema(other)
                            v.clear()
                            v.update(other)
                            continue

                        if (new_types := any_of_simple(any_of)) is not None:
                            v.clear()
                            v['type'] = new_types
                            continue

                        if NULL_TYPE in any_of:
                            any_of.remove(NULL_TYPE)

                    if all_of := v.get('allOf'):
                        if len(all_of) == 1:
                            v.clear()
                            v.update(all_of[0])
                            continue

                    if k == 'formFields':
                        # hack until we fix `customise_form_fields`
                        v.clear()
                        v.update({'items': {'$ref': '#/definitions/FormFieldProps'}, 'type': 'array'})
                        continue

                if k == 'enum':
                    s[k] = IsList(*v, check_order=False)

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

    model_properties = model_schema['properties']
    model_filled = set(model_schema.get('required', []))
    for key, value in model_properties.items():
        value.pop('title', None)
        if value.pop('default', None) is not None:
            model_filled.add(key)

    if title == 'Table':
        # special case for `Table` as `columns` is filled by a validator in pydantic
        model_filled.add('columns')
    elif title == 'Details':
        # same for `Details` and `fields`
        model_filled.add('fields')

    fix_pydantic_schema(model_properties)

    try:
        react_schema = REACT_SCHEMA_DEFS[f'{title}Props']
    except KeyError as e:
        pytest.fail(f'No react model found with name {e}')

    react_properties = react_schema['properties']
    react_required = set(react_schema.get('required', []))
    # typescript-json-schema adds type to `const` properties while pydantic does not,
    # pydantic matches the example from JSON Schema's docs
    # https://json-schema.org/understanding-json-schema/reference/const
    react_properties['type'].pop('type')
    # `onChange` is a frontend only attribute
    react_properties.pop('onChange', None)

    # ClassName is sometimes defined on props just to satisfy typescript, doesn't need to be included the model
    if 'className' not in model_properties:
        react_properties.pop('className', None)

    # see https://github.com/YousefED/typescript-json-schema/issues/583
    if key := next((k for k, v in react_properties.items() if v == {'$ref': '#/definitions/AnyEvent'}), None):
        react_properties[key] = REACT_SCHEMA_DEFS['AnyEvent']

    # debug(model_properties, react_properties)
    assert model_properties == react_properties

    assert model_filled == react_required
