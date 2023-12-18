from pathlib import Path
from typing import Literal
import typing_extensions

from pydantic import BaseModel

from fastui import FastUI
from fastui import class_name as _class_name
from fastui import events
from pydantic.json_schema import GenerateJsonSchema, JsonSchemaValue
from pydantic_core import to_json, core_schema


def is_type_schema(schema: core_schema.WithDefaultSchema) -> bool:
    inner = schema['schema']
    if inner.get('type') == 'literal':
        expected = inner['expected']
        if len(expected) == 1 and expected[0] == schema['default']:
            return True
    return False


class CustomGenerateJsonSchema(GenerateJsonSchema):
    # def generate_inner(self, schema) -> JsonSchemaValue:
    #     # debug(schema['type'], schema.keys())
    #     if schema.get('type') == 'tagged-union':
    #         if 'Div' in schema['choices'] and 'Text' in schema['choices']:
    #             schema['ref'] = 'fastui.components.AnyComponent'
    #     # debug(schema)
    #     return super().generate_inner(schema)

    def field_title_should_be_set(self, schema) -> bool:
        return False
        # if schema.get('type') == 'literal' and schema.get('expected') == [IsStr(regex='[A-Z].+')]:
        #     return False
        # return super().field_title_should_be_set(schema)

    def default_schema(self, schema: core_schema.WithDefaultSchema) -> JsonSchemaValue:
        inner = schema['schema']
        if is_type_schema(schema):
            return self.generate_inner(inner)

        if inner.get('type') == 'nullable' and inner.get('ref', '').startswith('fastui.class_name.ClassName:'):
            return self.generate_inner(inner)

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
            # elif 'Div' in choice_keys and 'Text' in choice_keys:
            #     schema['ref'] = 'fastui.components.AnyComponent'

        return super().tagged_union_schema(schema)


# Thing = typing_extensions.TypeAliasType('Thing', Literal['Div', 'Text'])
Thing = Literal['Div', 'Text']


class MyModel(BaseModel):
    x: int
    # type: Literal['MyModel'] = 'MyModel'
    t: Thing
    # class_name: _class_name.ClassNameField = None
    # trigger: events.AnyEvent = None


# test_schema = MyModel.model_json_schema(by_alias=True, mode='serialization', schema_generator=CustomGenerateJsonSchema)
# debug(test_schema)


fastui_schema = FastUI.model_json_schema(by_alias=True, mode='serialization', schema_generator=CustomGenerateJsonSchema)
Path('schema.json').write_bytes(to_json(fastui_schema, indent=2))

"""
Then run

npx json2ts schema.json models.ts --additionalProperties false --no-style.semi --style.singleQuote
"""
