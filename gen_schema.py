from pathlib import Path
from typing import Any

from fastui import FastUI
from pydantic.json_schema import GenerateJsonSchema, JsonSchemaValue
from pydantic_core import to_json, core_schema


def is_type_schema(schema: core_schema.WithDefaultSchema) -> bool:
    inner = schema['schema']
    if inner['type'] == 'literal':
        expected = inner['expected']
        if len(expected) == 1 and expected[0] == schema['default']:
            return True
    return False


class CustomGenerateJsonSchema(GenerateJsonSchema):
    def field_title_should_be_set(self, schema) -> bool:
        return False

    def default_schema(self, schema: core_schema.WithDefaultSchema) -> JsonSchemaValue:
        inner = schema['schema']
        if is_type_schema(schema):
            return self.generate_inner(inner)

        # if inner.get('type') == 'nullable' and inner.get('ref', '').startswith('fastui.class_name.ClassName:'):
        #     return self.generate_inner(inner)

        return super().default_schema(schema)

    def field_is_required(
            self,
            field: core_schema.ModelField | core_schema.DataclassField | core_schema.TypedDictField,
            total: bool,
    ) -> bool:
        inner = field['schema']
        if inner.get('type') == 'default' and is_type_schema(inner):
            return True
        return super().field_is_required(field, total)

    def nullable_schema(self, schema: core_schema.NullableSchema) -> JsonSchemaValue:
        null_schema = {'type': 'null'}
        inner_json_schema = self.generate_inner(schema['schema'])

        if inner_json_schema == null_schema:
            return null_schema
        else:
            # since we use `exclude_none=True`, field can't be null
            return inner_json_schema

    def tagged_union_schema(self, schema: core_schema.TaggedUnionSchema) -> JsonSchemaValue:
        if schema['discriminator'] == 'type':
            if 'go-to' in schema['choices']:
                schema['ref'] = 'fastui.events.AnyEvent'
        return super().tagged_union_schema(schema)


fastui_schema = FastUI.model_json_schema(by_alias=True, mode='serialization', schema_generator=CustomGenerateJsonSchema)
any_comp_def = fastui_schema['$defs']['Div']['properties']['components']['items'].copy()
any_comp_ref = {'$ref': '#/$defs/AnyComponent'}


def replace_any_comp(s: Any):
    if isinstance(s, dict):
        if s == any_comp_def:
            return any_comp_ref
        else:
            return {k: replace_any_comp(v) for k, v in s.items()}
    elif isinstance(s, list):
        return [replace_any_comp(v) for v in s]
    else:
        return s


fastui_schema['items'] = any_comp_ref
fastui_schema = replace_any_comp(fastui_schema)
fastui_schema['$defs']['AnyComponent'] = any_comp_def
Path('schema.json').write_bytes(to_json(fastui_schema, indent=2))

"""
Then run

npx json2ts schema.json models.ts --additionalProperties false --no-style.semi --style.singleQuote
"""
