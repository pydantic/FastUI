"""
Component definitions.

NOTE: all imports should be "simple" so name space of the module is polluted as little as possible.

All CamelCase names in the namespace should be components.
"""
from __future__ import annotations as _annotations

import typing
import pydantic

from . import extra, events


class Text(pydantic.BaseModel):
    text: str
    type: typing.Literal['Text'] = 'Text'


class Div(pydantic.BaseModel):
    children: list[AnyComponent]
    class_name: extra.ClassName | None = None
    type: typing.Literal['Div'] = 'Div'


class Container(pydantic.BaseModel):
    children: list[AnyComponent]
    class_name: extra.ClassName | None = None
    type: typing.Literal['Container'] = 'Container'


class Row(pydantic.BaseModel):
    children: list[AnyComponent]
    class_name: extra.ClassName | None = None
    type: typing.Literal['Row'] = 'Row'


class Col(pydantic.BaseModel):
    children: list[AnyComponent]
    class_name: extra.ClassName | None = None
    type: typing.Literal['Col'] = 'Col'


class Button(pydantic.BaseModel):
    text: str
    on_click: events.Event | None = pydantic.Field(None, serialization_alias='onClick')
    class_name: extra.ClassName | None = None
    type: typing.Literal['Button'] = 'Button'


class Modal(pydantic.BaseModel):
    title: str
    body: list[AnyComponent]
    footer: list[AnyComponent] | None = None
    open_trigger: events.PageEvent | None = pydantic.Field(None, serialization_alias='openTrigger')
    open: bool = False
    class_name: extra.ClassName | None = None
    type: typing.Literal['Modal'] = 'Modal'


AnyComponent = typing.Annotated[Text | Div | Container | Row | Col | Button | Modal, pydantic.Field(discriminator='type')]
