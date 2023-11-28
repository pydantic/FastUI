import enum
import typing
from abc import ABC

import annotated_types
import pydantic

from .. import class_name as _class_name
from .. import events

__all__ = 'DisplayMode', 'DisplayLookup', 'Display', 'Details'


class DisplayMode(enum.StrEnum):
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


class DisplayBase(pydantic.BaseModel, ABC, defer_build=True):
    mode: DisplayMode | None = None
    on_click: events.AnyEvent | None = pydantic.Field(default=None, serialization_alias='onClick')


class DisplayLookup(DisplayBase, extra='forbid'):
    """
    Description of how to display a value looked up from data, either in a table or detail view.
    """

    field: str
    title: str | None = None
    # percentage width - 0 to 100, specific to tables
    table_width_percent: typing.Annotated[int, annotated_types.Interval(ge=0, le=100)] | None = pydantic.Field(
        default=None, serialization_alias='tableWidthPercent'
    )


class Display(DisplayBase, extra='forbid'):
    """
    Description of how to display a value, either in a table or detail view.
    """

    value: typing.Any
    type: typing.Literal['Display'] = 'Display'


DataModel = typing.TypeVar('DataModel', bound=pydantic.BaseModel)


class Details(pydantic.BaseModel, typing.Generic[DataModel], extra='forbid'):
    data: DataModel
    fields: list[DisplayLookup] | None = None
    class_name: _class_name.ClassName = None
    type: typing.Literal['Details'] = 'Details'

    @pydantic.model_validator(mode='after')
    def fill_fields(self) -> typing.Self:
        if self.fields is None:
            self.fields = [
                DisplayLookup(field=name, title=field.title) for name, field in self.data.model_fields.items()
            ]
        else:
            # add pydantic titles to fields that don't have them
            for field in (c for c in self.fields if c.title is None):
                pydantic_field = self.data.model_fields.get(field.field)
                if pydantic_field and pydantic_field.title:
                    field.title = pydantic_field.title
        return self
