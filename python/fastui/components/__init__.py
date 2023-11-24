"""
Component definitions.

NOTE: all imports should be "simple" so name space of the module is polluted as little as possible.

All CamelCase names in the namespace should be components.
"""
from __future__ import annotations as _annotations

import typing

import pydantic

from .. import events
from . import extra
from .forms import Form, FormField, ModelForm
from .tables import Table, TableColumn

if typing.TYPE_CHECKING:
    import pydantic.fields

__all__ = (
    'AnyComponent',
    'Text',
    'Div',
    'Page',
    'Heading',
    'Row',
    'Col',
    'Button',
    'Modal',
    'ModelForm',
    'Form',
    'Table',
    'TableColumn',
)


class Text(pydantic.BaseModel, extra='forbid'):
    text: str
    type: typing.Literal['Text'] = 'Text'


class Paragraph(pydantic.BaseModel, extra='forbid'):
    text: str
    type: typing.Literal['Paragraph'] = 'Paragraph'


class PageTitle(pydantic.BaseModel, extra='forbid'):
    """
    This sets the title of the HTML page via the `document.title` property.
    """

    text: str
    type: typing.Literal['PageTitle'] = 'PageTitle'


class Div(pydantic.BaseModel, extra='forbid'):
    components: list[AnyComponent]
    class_name: extra.ClassName = None
    type: typing.Literal['Div'] = 'Div'


class Page(pydantic.BaseModel, extra='forbid'):
    """
    Similar to `container` in many UI frameworks, this should be a reasonable root component for most pages.
    """

    components: list[AnyComponent]
    class_name: extra.ClassName = None
    type: typing.Literal['Page'] = 'Page'


class Heading(pydantic.BaseModel, extra='forbid'):
    text: str
    level: typing.Literal[1, 2, 3, 4, 5, 6] = 1
    class_name: extra.ClassName = None
    type: typing.Literal['Heading'] = 'Heading'


class Button(pydantic.BaseModel, extra='forbid'):
    text: str
    on_click: events.AnyEvent | None = pydantic.Field(default=None, serialization_alias='onClick')
    html_type: typing.Literal['button', 'submit', 'reset'] | None = pydantic.Field(
        default=None, serialization_alias='htmlType'
    )
    class_name: extra.ClassName = None
    type: typing.Literal['Button'] = 'Button'


class Link(pydantic.BaseModel, extra='forbid'):
    components: list[AnyComponent]
    on_click: events.AnyEvent | None = pydantic.Field(default=None, serialization_alias='onClick')
    mode: typing.Literal['navbar', 'tabs', 'vertical'] | None = None
    active: bool | str | None = None
    class_name: extra.ClassName = None
    type: typing.Literal['Link'] = 'Link'


class LinkList(pydantic.BaseModel, extra='forbid'):
    links: list[Link]
    mode: typing.Literal['tabs', 'vertical'] | None = None
    class_name: extra.ClassName = None
    type: typing.Literal['LinkList'] = 'LinkList'


class Navbar(pydantic.BaseModel, extra='forbid'):
    title: str | None = None
    title_event: events.AnyEvent | None = pydantic.Field(default=None, serialization_alias='titleEvent')
    links: list[Link] = pydantic.Field(default_factory=list)
    class_name: extra.ClassName = None
    type: typing.Literal['Navbar'] = 'Navbar'


class Modal(pydantic.BaseModel, extra='forbid'):
    title: str
    body: list[AnyComponent]
    footer: list[AnyComponent] | None = None
    open_trigger: events.PageEvent | None = pydantic.Field(default=None, serialization_alias='openTrigger')
    open: bool = False
    class_name: extra.ClassName = None
    type: typing.Literal['Modal'] = 'Modal'


class ServerLoad(pydantic.BaseModel, extra='forbid'):
    """
    A component that will be replaced by the server with the component returned by the given URL.
    """

    url: str
    class_name: extra.ClassName = None
    type: typing.Literal['ServerLoad'] = 'ServerLoad'


AnyComponent = typing.Annotated[
    Text
    | Paragraph
    | PageTitle
    | Div
    | Page
    | Heading
    | Button
    | Link
    | LinkList
    | Navbar
    | Modal
    | ServerLoad
    | Table
    | Form
    | ModelForm
    | FormField,
    pydantic.Field(discriminator='type'),
]
