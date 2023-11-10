from __future__ import annotations as _annotations

import typing
from enum import StrEnum

import pydantic

from . import extra, events

# TODO allow dataclasses and dicts here too
DataModel = typing.TypeVar('DataModel', bound=pydantic.BaseModel)


class Display(StrEnum):
    """
    How to a value.
    """
    auto = 'auto'  # default, same as None below
    plain = 'plain'
    datetime = 'datetime'
    date = 'date'
    duration = 'duration'
    as_title = 'as_title'
    markdown = 'markdown'
    json = 'json'
    inline_code = 'inline_code'


class Column(pydantic.BaseModel):
    """
    Description of a table column.
    """
    field: str
    display: Display | None = None
    title: str | None = None
    event: events.Event | None = None
    class_name: extra.ClassName | None = None


class Table(pydantic.BaseModel, typing.Generic[DataModel]):
    data: list[DataModel]
    columns: list[Column] | None = None
    # TODO pagination
    class_name: extra.ClassName | None = None
    type: typing.Literal['Table'] = 'Table'

    @pydantic.field_validator('columns')
    def fill_columns(cls, columns: list[Column] | None, info: pydantic.ValidationInfo) -> list[Column] | None:
        data = info.data.get('data', [])
        try:
            data_model_0 = data[0]
        except IndexError:
            return columns

        if columns is None:
            return [Column(field=name, title=field.title) for name, field in data_model_0.model_fields.items()]
        else:
            # add pydantic titles to columns that don't have them
            for column in (c for c in columns if c.title is None):
                field = data_model_0.model_fields.get(column.field)
                if field and field.title:
                    column.title = field.title
            return columns
