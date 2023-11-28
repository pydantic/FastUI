from __future__ import annotations as _annotations

import typing

import annotated_types
import pydantic

from .. import events
from ..display import Display
from . import extra

# TODO allow dataclasses and dicts here too
DataModel = typing.TypeVar('DataModel', bound=pydantic.BaseModel)
Percentage: typing.TypeAlias = typing.Annotated[int, annotated_types.Interval(ge=0, le=100)]


class TableColumn(pydantic.BaseModel, extra='forbid'):
    """
    Description of a table column.
    """

    field: str
    display: Display | None = None
    title: str | None = None
    on_click: typing.Annotated[events.AnyEvent | None, pydantic.Field(serialization_alias='onClick')] = None
    # percentage width - 0 to 100
    width_percent: Percentage | None = pydantic.Field(default=None, serialization_alias='widthPercent')
    class_name: extra.ClassName | None = None


class Table(pydantic.BaseModel, typing.Generic[DataModel], extra='forbid'):
    data: list[DataModel]
    columns: list[TableColumn] | None = None
    # TODO pagination
    class_name: extra.ClassName | None = None
    type: typing.Literal['Table'] = 'Table'

    @pydantic.model_validator(mode='after')
    def fill_columns(self) -> typing.Self:
        try:
            data_model_0 = self.data[0]
        except IndexError:
            return self

        if self.columns is None:
            self.columns = [
                TableColumn(field=name, title=field.title) for name, field in data_model_0.model_fields.items()
            ]
        else:
            # add pydantic titles to columns that don't have them
            for column in (c for c in self.columns if c.title is None):
                field = data_model_0.model_fields.get(column.field)
                if field and field.title:
                    column.title = field.title
        return self


class Pagination(pydantic.BaseModel):
    page: int
    page_size: int
    total: int
    class_name: extra.ClassName | None = None
    type: typing.Literal['Pagination'] = 'Pagination'

    @pydantic.computed_field(alias='pageCount')
    def page_count(self) -> int:
        return (self.total - 1) // self.page_size + 1
