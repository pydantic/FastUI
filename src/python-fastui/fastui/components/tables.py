import typing as _t

import pydantic
from pydantic_core import core_schema as _core_schema

from .. import class_name as _class_name
from .. import types as _types
from . import display

# TODO allow dataclasses and typed dicts here too


class Table(pydantic.BaseModel, extra='forbid'):
    data: _t.Sequence[_types.DataModel]
    columns: _t.Union[_t.List[display.DisplayLookup], None] = None
    data_model: _t.Union[_t.Type[pydantic.BaseModel], None] = pydantic.Field(default=None, exclude=True)
    no_data_message: _t.Union[str, None] = pydantic.Field(default=None, serialization_alias='noDataMessage')
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['Table'] = 'Table'

    @pydantic.field_serializer('columns')
    def _fill_columns(self, columns: _t.Union[_t.List[display.DisplayLookup], None]) -> _t.List[display.DisplayLookup]:
        if self.data_model:
            data_model_type = self.data_model
        else:
            try:
                data_model_type = self.data[0]
            except IndexError:
                raise ValueError('Cannot infer model from empty data, please set `Table(..., model=MyModel)`')

        if columns is None:
            return [
                display.DisplayLookup(field=name, title=field.title)
                for name, field in data_model_type.model_fields.items()
            ]
        else:
            # add pydantic titles to columns that don't have them
            for column in (c for c in columns if c.title is None):
                field = data_model_type.model_fields.get(column.field)
                if field and field.title:
                    column.title = field.title
            return columns

    @pydantic.field_serializer('data')
    def _serialize_data(self, v: _t.List[_types.DataModel]) -> _t.List[_t.Dict[str, _types.JsonData]]:
        # waiting for a https://github.com/pydantic/pydantic/issues/6423 flag
        return [row.model_dump(by_alias=True) for row in v]

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: _core_schema.CoreSchema, handler: pydantic.GetJsonSchemaHandler
    ) -> _t.Any:
        json_schema = handler(core_schema)
        schema_def = handler.resolve_ref_schema(json_schema)
        # columns are filled by `_fill_columns`
        schema_def['required'].append('columns')
        # the idea here is to revert the return type of `_serialize_data` changing the schema for `data`
        # TODO this is super hacky, but it gives use the right schema, can we do better
        schema_def['properties']['data'] = {
            'type': 'array',
            'items': {
                '$ref': '#/$defs/DataModel-Output__1',
            },
        }
        return json_schema


class Pagination(pydantic.BaseModel):
    page: int
    page_size: int = pydantic.Field(serialization_alias='pageSize')
    total: int
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['Pagination'] = 'Pagination'

    @pydantic.computed_field(alias='pageCount')
    def page_count(self) -> int:
        return (self.total - 1) // self.page_size + 1
