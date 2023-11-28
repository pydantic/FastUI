from __future__ import annotations as _annotations

import typing

import pydantic

from .. import class_name as _class_name
from . import display

# TODO allow dataclasses and typed dicts here too
DataModel = typing.TypeVar('DataModel', bound=pydantic.BaseModel)


class Table(pydantic.BaseModel, typing.Generic[DataModel], extra='forbid'):
    data: list[DataModel]
    columns: list[display.DisplayLookup] | None = None
    no_data_message: str | None = pydantic.Field(default=None, serialization_alias='noDataMessage')
    class_name: _class_name.ClassName = None
    type: typing.Literal['Table'] = 'Table'

    @pydantic.model_validator(mode='after')
    def fill_columns(self) -> typing.Self:
        args = self.__pydantic_generic_metadata__['args']
        try:
            data_model_type: type[DataModel] = args[0]
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


class Pagination(pydantic.BaseModel):
    page: int
    page_size: int
    total: int
    class_name: _class_name.ClassName = None
    type: typing.Literal['Pagination'] = 'Pagination'

    @pydantic.computed_field(alias='pageCount')
    def page_count(self) -> int:
        return (self.total - 1) // self.page_size + 1
