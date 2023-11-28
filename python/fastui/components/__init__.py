"""
Component definitions.

NOTE: all imports should be "simple" so name space of the module is polluted as little as possible.

All CamelCase names in the namespace should be components.
"""
from __future__ import annotations as _annotations

import typing

import pydantic

from .. import class_name as _class_name
from .. import events
from .display import Details, Display
from .forms import (
    Form,
    FormField,
    FormFieldCheckbox,
    FormFieldFile,
    FormFieldInput,
    FormFieldSelect,
    FormFieldSelectSearch,
    ModelForm,
)
from .tables import Pagination, Table

if typing.TYPE_CHECKING:
    import pydantic.fields

__all__ = (
    'AnyComponent',
    'Text',
    'Div',
    'Page',
    'Heading',
    'Button',
    'Modal',
    'ModelForm',
    'FormFieldInput',
    'FormFieldCheckbox',
    'FormFieldFile',
    'FormFieldSelect',
    'FormFieldSelectSearch',
    'Form',
    'Table',
    'Display',
    'Details',
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
    class_name: _class_name.ClassName = None
    type: typing.Literal['Div'] = 'Div'


class Page(pydantic.BaseModel, extra='forbid'):
    """
    Similar to `container` in many UI frameworks, this should be a reasonable root component for most pages.
    """

    components: list[AnyComponent]
    class_name: _class_name.ClassName = None
    type: typing.Literal['Page'] = 'Page'


class Heading(pydantic.BaseModel, extra='forbid'):
    text: str
    level: typing.Literal[1, 2, 3, 4, 5, 6] = 1
    html_id: str | None = pydantic.Field(default=None, serialization_alias='htmlId')
    class_name: _class_name.ClassName = None
    type: typing.Literal['Heading'] = 'Heading'


# see https://github.com/PrismJS/prism-themes
# and https://cdn.jsdelivr.net/npm/react-syntax-highlighter@15.5.0/dist/esm/styles/prism/index.js
CodeStyle = typing.Annotated[str | None, pydantic.Field(serialization_alias='codeStyle')]


class Markdown(pydantic.BaseModel, extra='forbid'):
    text: str
    code_style: CodeStyle = None
    class_name: _class_name.ClassName = None
    type: typing.Literal['Markdown'] = 'Markdown'


class Code(pydantic.BaseModel, extra='forbid'):
    text: str
    language: str | None = None
    code_style: CodeStyle = None
    class_name: _class_name.ClassName = None
    type: typing.Literal['Code'] = 'Code'


class Button(pydantic.BaseModel, extra='forbid'):
    text: str
    on_click: events.AnyEvent | None = pydantic.Field(default=None, serialization_alias='onClick')
    html_type: typing.Literal['button', 'submit', 'reset'] | None = pydantic.Field(
        default=None, serialization_alias='htmlType'
    )
    class_name: _class_name.ClassName = None
    type: typing.Literal['Button'] = 'Button'


class Link(pydantic.BaseModel, extra='forbid'):
    components: list[AnyComponent]
    on_click: events.AnyEvent | None = pydantic.Field(default=None, serialization_alias='onClick')
    mode: typing.Literal['navbar', 'tabs', 'vertical', 'pagination'] | None = None
    active: bool | str | None = None
    locked: bool | None = None
    class_name: _class_name.ClassName = None
    type: typing.Literal['Link'] = 'Link'


class LinkList(pydantic.BaseModel, extra='forbid'):
    links: list[Link]
    mode: typing.Literal['tabs', 'vertical', 'pagination'] | None = None
    class_name: _class_name.ClassName = None
    type: typing.Literal['LinkList'] = 'LinkList'


class Navbar(pydantic.BaseModel, extra='forbid'):
    title: str | None = None
    title_event: events.AnyEvent | None = pydantic.Field(default=None, serialization_alias='titleEvent')
    links: list[Link] = pydantic.Field(default_factory=list)
    class_name: _class_name.ClassName = None
    type: typing.Literal['Navbar'] = 'Navbar'


class Modal(pydantic.BaseModel, extra='forbid'):
    title: str
    body: list[AnyComponent]
    footer: list[AnyComponent] | None = None
    open_trigger: events.PageEvent | None = pydantic.Field(default=None, serialization_alias='openTrigger')
    open_context: events.EventContext | None = pydantic.Field(default=None, serialization_alias='openContext')
    class_name: _class_name.ClassName = None
    type: typing.Literal['Modal'] = 'Modal'


class ServerLoad(pydantic.BaseModel, extra='forbid'):
    """
    A component that will be replaced by the server with the component returned by the given URL.
    """

    path: str
    load_trigger: events.PageEvent | None = pydantic.Field(default=None, serialization_alias='loadTrigger')
    components: list[AnyComponent] | None = None
    sse: bool | None = None
    type: typing.Literal['ServerLoad'] = 'ServerLoad'


AnyComponent = typing.Annotated[
    Text
    | Paragraph
    | PageTitle
    | Div
    | Page
    | Heading
    | Markdown
    | Code
    | Button
    | Link
    | LinkList
    | Navbar
    | Modal
    | ServerLoad
    | Table
    | Pagination
    | Display
    | Details
    | Form
    | ModelForm
    | FormField,
    pydantic.Field(discriminator='type'),
]
