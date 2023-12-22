import typing as _t

import pydantic
import typing_extensions as _te
from pydantic_core import core_schema as _core_schema

from .. import class_name as _class_name
from .. import types as _types
from . import display

# TODO allow dataclasses and typed dicts here too


class Table(pydantic.BaseModel, extra='forbid'):
    data: _t.Sequence[pydantic.SerializeAsAny[_types.DataModel]]
    columns: _t.Union[_t.List[display.DisplayLookup], None] = None
    data_model: _t.Union[_t.Type[pydantic.BaseModel], None] = pydantic.Field(default=None, exclude=True)
    no_data_message: _t.Union[str, None] = pydantic.Field(default=None, serialization_alias='noDataMessage')
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['Table'] = 'Table'

    @pydantic.model_validator(mode='after')
    def _fill_columns(self) -> _te.Self:
        if self.data_model:
            data_model_type = self.data_model
        else:
            try:
                data_model_type = type(self.data[0])
            except IndexError:
                raise ValueError('Cannot infer model from empty data, please set `Table(..., model=MyModel)`')

        if self.columns is None:
            self.columns = [
                display.DisplayLookup(field=name, title=field.title)
                for name, field in data_model_type.model_fields.items()
            ]
        else:
            # add pydantic titles to columns that don't have them
            for column in (c for c in self.columns if c.title is None):
                field = data_model_type.model_fields.get(column.field)
                if field and field.title:
                    column.title = field.title
        return self

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: _core_schema.CoreSchema, handler: pydantic.GetJsonSchemaHandler
    ) -> _t.Any:
        json_schema = handler(core_schema)
        schema_def = handler.resolve_ref_schema(json_schema)
        # columns are filled by `_fill_columns`
        schema_def['required'].append('columns')
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
