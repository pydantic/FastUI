import re
import subprocess
from pathlib import Path
from typing import Any, cast

from pydantic import ImportString, TypeAdapter
from pydantic.json_schema import GenerateJsonSchema, JsonSchemaValue
from pydantic_core import core_schema, to_json

THIS_DIR = Path(__file__).parent


def main(python_object_str: str, typescript_output_file: Path):
    python_object = TypeAdapter(ImportString).validate_python(python_object_str)
    fastui_schema = TypeAdapter(python_object).json_schema(
        by_alias=True, mode='serialization', schema_generator=CustomGenerateJsonSchema
    )
    # the following post-processing is a workaround for
    # https://github.com/pydantic/pydantic/issues/8320
    any_comp_def = fastui_schema['$defs']['Div']['properties']['components']['items'].copy()
    any_comp_ref = {'$ref': '#/$defs/FastProps'}

    def replace_any_comp(value: Any) -> Any:
        if isinstance(value, dict):
            if value == any_comp_def:
                return any_comp_ref
            else:
                return {k: replace_any_comp(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [replace_any_comp(v) for v in value]
        else:
            return value

    fastui_schema['items'] = any_comp_ref
    fastui_schema = replace_any_comp(fastui_schema)
    fastui_schema['$defs']['FastProps'] = any_comp_def
    fastui_schema.pop('description')

    json_schema_file = Path('fastui-json-schema.json')
    json_schema_file.write_bytes(to_json(fastui_schema, indent=2))
    json2ts(json_schema_file, typescript_output_file)


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
        if inner['type'] == 'default' and is_type_schema(cast(core_schema.WithDefaultSchema, inner)):
            return True
        else:
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


def is_type_schema(schema: core_schema.WithDefaultSchema) -> bool:
    inner = schema['schema']
    if inner['type'] == 'literal':
        expected = cast(core_schema.LiteralSchema, inner)['expected']
        if len(expected) == 1 and expected[0] == schema.get('default', object()):
            return True
    return False


TS_PREFIX = b"""\
/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify python types, then run
 * `fastui generate <python-object> <typescript-output-file>`.
 */"""


def json2ts(input_file: Path, output_file: Path):
    args = (
        'npx',
        'json2ts',
        str(input_file),
        str(output_file),
        '--additionalProperties',
        'false',
        '--no-style.semi',
        '--style.singleQuote',
        '--no-unknownAny',
    )
    try:
        subprocess.run(args, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise RuntimeError(
            "Failed to run json2ts, you'll need to install `npx` and `json-schema-to-typescript`, "
            f"then run the command:\n\n    {' '.join(args)}\n\n"
        ) from e
    else:
        assert output_file.is_file()
        # remove the root list type that we don't need
        output = (
            output_file.read_bytes()
            .replace(b'export type FastUI = FastProps[]\n', b'')
            .replace(b'/* eslint-disable */\n', b'')
        )
        output = re.sub(rb'/\*\*\s+\* This file was automatically generated.+?\*/', TS_PREFIX, output, flags=re.DOTALL)
        output_file.write_bytes(output)
        input_file.unlink()