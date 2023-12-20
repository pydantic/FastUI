import typing as _t

import pydantic
import typing_extensions as _te
from pydantic_core import core_schema as _core_schema

from .. import class_name as _class_name
from .. import types as _types
from . import display

# TODO allow dataclasses and typed dicts here too


class Table(pydantic.BaseModel, _t.Generic[_types.DataModelGeneric], extra='forbid'):
    data: _t.List[_types.DataModelGeneric]
    columns: _t.Union[_t.List[display.DisplayLookup], None] = None
    no_data_message: _t.Union[str, None] = pydantic.Field(default=None, serialization_alias='noDataMessage')
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['Table'] = 'Table'

    @pydantic.model_validator(mode='after')
    def fill_columns(self) -> _te.Self:
        args = self.__pydantic_generic_metadata__['args']
        try:
            data_model_type: _t.Type[_types.DataModelGeneric] = args[0]
        except IndexError:
            raise ValueError('`Table` must be parameterized with a pydantic model, i.e. `Table[MyModel]()`.')

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
        # columns are filled by `fill_columns`
        schema_def = handler.resolve_ref_schema(json_schema)
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
