"""
Component definitions.

NOTE: all imports should be "simple" so name space of the module is polluted as little as possible.

All CamelCase names in the namespace should be components.
"""
import typing as _t

import pydantic
import typing_extensions as _te

from .. import class_name as _class_name
from .. import events
from .display import Details, Display
from .forms import (
    Form,
    FormField,
    FormFieldBoolean,
    FormFieldFile,
    FormFieldInput,
    FormFieldSelect,
    FormFieldSelectSearch,
    ModelForm,
)
from .tables import Pagination, Table

if _t.TYPE_CHECKING:
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
    'FormFieldBoolean',
    'FormFieldFile',
    'FormFieldSelect',
    'FormFieldSelectSearch',
    'Form',
    'Table',
    'Display',
    'Details',
    'Image',
)


class Text(pydantic.BaseModel, extra='forbid'):
    text: str
    type: _t.Literal['Text'] = 'Text'


class Paragraph(pydantic.BaseModel, extra='forbid'):
    text: str
    class_name: _class_name.ClassName = None
    type: _t.Literal['Paragraph'] = 'Paragraph'


class PageTitle(pydantic.BaseModel, extra='forbid'):
    """
    This sets the title of the HTML page via the `document.title` property.
    """

    text: str
    type: _t.Literal['PageTitle'] = 'PageTitle'


class Div(pydantic.BaseModel, extra='forbid'):
    components: '_t.List[AnyComponent]'
    class_name: _class_name.ClassName = None
    type: _t.Literal['Div'] = 'Div'


class Page(pydantic.BaseModel, extra='forbid'):
    """
    Similar to `container` in many UI frameworks, this should be a reasonable root component for most pages.
    """

    components: '_t.List[AnyComponent]'
    class_name: _class_name.ClassName = None
    type: _t.Literal['Page'] = 'Page'


class Heading(pydantic.BaseModel, extra='forbid'):
    text: str
    level: _t.Literal[1, 2, 3, 4, 5, 6] = 1
    html_id: _t.Union[str, None] = pydantic.Field(default=None, serialization_alias='htmlId')
    class_name: _class_name.ClassName = None
    type: _t.Literal['Heading'] = 'Heading'


# see https://github.com/PrismJS/prism-themes
# and https://cdn.jsdelivr.net/npm/react-syntax-highlighter@15.5.0/dist/esm/styles/prism/index.js
CodeStyle = _te.Annotated[_t.Union[str, None], pydantic.Field(serialization_alias='codeStyle')]


class Markdown(pydantic.BaseModel, extra='forbid'):
    text: str
    code_style: CodeStyle = None
    class_name: _class_name.ClassName = None
    type: _t.Literal['Markdown'] = 'Markdown'


class Code(pydantic.BaseModel, extra='forbid'):
    text: str
    language: _t.Union[str, None] = None
    code_style: CodeStyle = None
    class_name: _class_name.ClassName = None
    type: _t.Literal['Code'] = 'Code'


class Button(pydantic.BaseModel, extra='forbid'):
    text: str
    on_click: _t.Union[events.AnyEvent, None] = pydantic.Field(default=None, serialization_alias='onClick')
    html_type: _t.Union[_t.Literal['button', 'submit', 'reset'], None] = pydantic.Field(
        default=None, serialization_alias='htmlType'
    )
    class_name: _class_name.ClassName = None
    type: _t.Literal['Button'] = 'Button'


class Link(pydantic.BaseModel, extra='forbid'):
    components: '_t.List[AnyComponent]'
    on_click: _t.Union[events.AnyEvent, None] = pydantic.Field(default=None, serialization_alias='onClick')
    mode: _t.Union[_t.Literal['navbar', 'tabs', 'vertical', 'pagination'], None] = None
    active: _t.Union[bool, str, None] = None
    locked: _t.Union[bool, None] = None
    class_name: _class_name.ClassName = None
    type: _t.Literal['Link'] = 'Link'


class LinkList(pydantic.BaseModel, extra='forbid'):
    links: _t.List[Link]
    mode: _t.Union[_t.Literal['tabs', 'vertical', 'pagination'], None] = None
    class_name: _class_name.ClassName = None
    type: _t.Literal['LinkList'] = 'LinkList'


class Navbar(pydantic.BaseModel, extra='forbid'):
    title: _t.Union[str, None] = None
    title_event: _t.Union[events.AnyEvent, None] = pydantic.Field(default=None, serialization_alias='titleEvent')
    links: _t.List[Link] = pydantic.Field(default_factory=list)
    class_name: _class_name.ClassName = None
    type: _t.Literal['Navbar'] = 'Navbar'


class Modal(pydantic.BaseModel, extra='forbid'):
    title: str
    body: '_t.List[AnyComponent]'
    footer: '_t.Union[_t.List[AnyComponent], None]' = None
    open_trigger: _t.Union[events.PageEvent, None] = pydantic.Field(default=None, serialization_alias='openTrigger')
    open_context: _t.Union[events.EventContext, None] = pydantic.Field(default=None, serialization_alias='openContext')
    class_name: _class_name.ClassName = None
    type: _t.Literal['Modal'] = 'Modal'


class ServerLoad(pydantic.BaseModel, extra='forbid'):
    """
    A component that will be replaced by the server with the component returned by the given URL.
    """

    path: str
    load_trigger: _t.Union[events.PageEvent, None] = pydantic.Field(default=None, serialization_alias='loadTrigger')
    components: '_t.Union[_t.List[AnyComponent], None]' = None
    sse: _t.Union[bool, None] = None
    type: _t.Literal['ServerLoad'] = 'ServerLoad'


class Image(pydantic.BaseModel, extra='forbid'):
    src: str
    alt: _t.Union[str, None] = None
    width: _t.Union[int, float, str, None] = None
    height: _t.Union[int, float, str, None] = None
    referrerpolicy: _t.Union[
        _t.Literal[
            'no-referrer',
            'no-referrer-when-downgrade',
            'origin',
            'origin-when-cross-origin',
            'same-origin',
            'strict-origin',
            'strict-origin-when-cross-origin',
            'unsafe-url',
        ],
        None,
    ] = None
    loading: _t.Union[_t.Literal['eager', 'lazy'], None] = None
    on_click: _t.Union[events.AnyEvent, None] = pydantic.Field(default=None, serialization_alias='onClick')
    class_name: _class_name.ClassName = None
    type: _t.Literal['Image'] = 'Image'


class Iframe(pydantic.BaseModel, extra='forbid'):
    src: pydantic.HttpUrl
    title: _t.Union[str, None] = None
    width: _t.Union[str, int, None] = None
    height: _t.Union[str, int, None] = None
    type: _t.Literal['Iframe'] = 'Iframe'


AnyComponent = _te.Annotated[
    _t.Union[
        Text,
        Paragraph,
        PageTitle,
        Div,
        Page,
        Heading,
        Markdown,
        Code,
        Button,
        Link,
        LinkList,
        Navbar,
        Modal,
        ServerLoad,
        Table,
        Pagination,
        Display,
        Details,
        Form,
        ModelForm,
        Image,
        Iframe,
        FormField,
    ],
    pydantic.Field(discriminator='type'),
]
