import typing as _t

import pydantic
import typing_extensions as _te
from pydantic.json_schema import CoreRef, GenerateJsonSchema, JsonRef
from pydantic_core import core_schema

IS_PYDANTIC_211_OR_GREATER = tuple(int(v) for v in pydantic.VERSION.split('.')[:2]) >= (2, 11)


# TODO: replace with https://docs.pydantic.dev/dev/api/types/#pydantic.types.JsonValue, maybe?
class JsonDataSchema:
    @staticmethod
    def __get_pydantic_json_schema__(
        _core_schema: core_schema.CoreSchema, handler: pydantic.GetJsonSchemaHandler
    ) -> _t.Any:
        json_data_schema = core_schema.union_schema(
            [
                core_schema.str_schema(),
                core_schema.float_schema(),
                core_schema.bool_schema(),
                core_schema.none_schema(),
                core_schema.list_schema(core_schema.definition_reference_schema('JsonData')),
                core_schema.dict_schema(core_schema.str_schema(), core_schema.definition_reference_schema('JsonData')),
            ],
            ref='JsonData',
        )
        rv = handler(json_data_schema)
        if IS_PYDANTIC_211_OR_GREATER:
            # Terrible hack. This is mimicking `GenerateJsonSchema.generate_inner.<locals>.populate_defs()`,
            # which used to be called in some place until 2.11, where the call was removed by
            # https://github.com/pydantic/pydantic/pull/11475.
            # The approach taken by this `JsonDataSchema` annotation (manually setting references) isn't viable,
            # but Pydantic is missing proper semantics on the behavior of core schema references
            gen_js_schema = _t.cast(GenerateJsonSchema, handler.generate_json_schema)  # type: ignore
            defs_ref, ref_json_schema = gen_js_schema.get_cache_defs_ref_schema(CoreRef('JsonData'))
            json_ref = JsonRef(ref_json_schema['$ref'])
            if rv.get('$ref', None) != json_ref:
                gen_js_schema.definitions[defs_ref] = rv
            rv = ref_json_schema
        return rv


JsonData = _te.Annotated[_t.Any, JsonDataSchema()]


class PydanticModelSchema:
    @staticmethod
    def __get_pydantic_json_schema__(
        _core_schema: core_schema.CoreSchema, handler: pydantic.GetJsonSchemaHandler
    ) -> _t.Any:
        model_json_schema = core_schema.dict_schema(
            core_schema.str_schema(),
            core_schema.definition_reference_schema('JsonData'),
            ref='DataModel',
        )
        rv = handler(model_json_schema)
        if IS_PYDANTIC_211_OR_GREATER:
            # Terrible hack. This is mimicking `GenerateJsonSchema.generate_inner.<locals>.populate_defs()`,
            # which used to be called in some place until 2.11, where the call was removed by
            # https://github.com/pydantic/pydantic/pull/11475.
            # The approach taken by this `PydanticModelSchema` annotation (manually setting references) isn't viable,
            # but Pydantic is missing proper semantics on the behavior of core schema references
            gen_js_schema = _t.cast(GenerateJsonSchema, handler.generate_json_schema)  # type: ignore
            defs_ref, ref_json_schema = gen_js_schema.get_cache_defs_ref_schema(CoreRef('DataModel'))
            json_ref = JsonRef(ref_json_schema['$ref'])
            if rv.get('$ref', None) != json_ref:
                gen_js_schema.definitions[defs_ref] = rv
            rv = ref_json_schema
        return rv


DataModel = _te.Annotated[pydantic.BaseModel, PydanticModelSchema()]
DataModelGeneric = _t.TypeVar('DataModelGeneric', bound=DataModel)
