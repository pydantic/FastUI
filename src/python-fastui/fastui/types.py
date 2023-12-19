import typing as _t

import pydantic
import typing_extensions as _te
from pydantic_core import core_schema


class JsonDataSchema:
    @staticmethod
    def __get_pydantic_core_schema__(*args: _t.Any) -> core_schema.CoreSchema:
        return core_schema.any_schema()

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
        return handler(json_data_schema)


_JsonData: _te.TypeAlias = '_t.Union[None, float, int, str, _t.List[_JsonData], _t.Dict[str, _JsonData]]'
JsonData = _te.Annotated[_JsonData, JsonDataSchema()]


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
        return handler(model_json_schema)


DataModel = _te.Annotated[pydantic.BaseModel, PydanticModelSchema()]
DataModelGeneric = _t.TypeVar('DataModelGeneric', bound=DataModel)
