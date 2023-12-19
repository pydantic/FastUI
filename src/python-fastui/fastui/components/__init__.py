"""
Component definitions.

NOTE: all imports should be "simple" so the namespace of the module is polluted as little as possible.

All CamelCase names in the namespace should be components.
"""
import typing as _t

import pydantic as _p
import typing_extensions as _te

from .. import class_name as _class_name
from .. import events, json_schema
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

__all__ = (
    # first we include everything from `AnyComponent`
    'Text',
    'Paragraph',
    'PageTitle',
    'Div',
    'Page',
    'Heading',
    'Markdown',
    'Code',
    'Json',
    'Button',
    'Link',
    'LinkList',
    'Navbar',
    'Modal',
    'ServerLoad',
    'Image',
    'Iframe',
    'Custom',
    'Table',
    'Pagination',
    'Display',
    'Details',
    'Form',
    'FormField',
    'ModelForm',
    # then `AnyComponent` itself
    'AnyComponent',
    # then the other form field types which are included in `AnyComponent` via the `FormField` union
    'FormFieldBoolean',
    'FormFieldFile',
    'FormFieldInput',
    'FormFieldSelect',
    'FormFieldSelectSearch',
)


class Text(_p.BaseModel, extra='forbid'):
    text: str
    type: _t.Literal['Text'] = 'Text'


class Paragraph(_p.BaseModel, extra='forbid'):
    text: str
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['Paragraph'] = 'Paragraph'


class PageTitle(_p.BaseModel, extra='forbid'):
    """
    This sets the title of the HTML page via the `document.title` property.
    """

    text: str
    type: _t.Literal['PageTitle'] = 'PageTitle'


class Div(_p.BaseModel, extra='forbid'):
    components: '_t.List[AnyComponent]'
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['Div'] = 'Div'


class Page(_p.BaseModel, extra='forbid'):
    """
    Similar to `container` in many UI frameworks, this should be a reasonable root component for most pages.
    """

    components: '_t.List[AnyComponent]'
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['Page'] = 'Page'


class Heading(_p.BaseModel, extra='forbid'):
    text: str
    level: _t.Literal[1, 2, 3, 4, 5, 6] = 1
    html_id: _t.Union[str, None] = _p.Field(default=None, serialization_alias='htmlId')
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['Heading'] = 'Heading'


# see https://github.com/PrismJS/prism-themes
# and https://cdn.jsdelivr.net/npm/react-syntax-highlighter@15.5.0/dist/esm/styles/prism/index.js
CodeStyle = _te.Annotated[_t.Union[str, None], _p.Field(serialization_alias='codeStyle')]


class Markdown(_p.BaseModel, extra='forbid'):
    text: str
    code_style: CodeStyle = None
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['Markdown'] = 'Markdown'


class Code(_p.BaseModel, extra='forbid'):
    text: str
    language: _t.Union[str, None] = None
    code_style: CodeStyle = None
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['Code'] = 'Code'


class Json(_p.BaseModel, extra='forbid'):
    value: json_schema.JsonData
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['JSON'] = 'JSON'


class Button(_p.BaseModel, extra='forbid'):
    text: str
    on_click: _t.Union[events.AnyEvent, None] = _p.Field(default=None, serialization_alias='onClick')
    html_type: _t.Union[_t.Literal['button', 'reset', 'submit'], None] = _p.Field(
        default=None, serialization_alias='htmlType'
    )
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['Button'] = 'Button'


class Link(_p.BaseModel, extra='forbid'):
    components: '_t.List[AnyComponent]'
    on_click: _t.Union[events.AnyEvent, None] = _p.Field(default=None, serialization_alias='onClick')
    mode: _t.Union[_t.Literal['navbar', 'tabs', 'vertical', 'pagination'], None] = None
    active: _t.Union[str, bool, None] = None
    locked: _t.Union[bool, None] = None
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['Link'] = 'Link'


class LinkList(_p.BaseModel, extra='forbid'):
    links: _t.List[Link]
    mode: _t.Union[_t.Literal['tabs', 'vertical', 'pagination'], None] = None
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['LinkList'] = 'LinkList'


class Navbar(_p.BaseModel, extra='forbid'):
    title: _t.Union[str, None] = None
    title_event: _t.Union[events.AnyEvent, None] = _p.Field(default=None, serialization_alias='titleEvent')
    links: _t.List[Link] = _p.Field(default=[])
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['Navbar'] = 'Navbar'


class Modal(_p.BaseModel, extra='forbid'):
    title: str
    body: '_t.List[AnyComponent]'
    footer: '_t.Union[_t.List[AnyComponent], None]' = None
    open_trigger: _t.Union[events.PageEvent, None] = _p.Field(default=None, serialization_alias='openTrigger')
    open_context: _t.Union[events.ContextType, None] = _p.Field(default=None, serialization_alias='openContext')
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['Modal'] = 'Modal'


class ServerLoad(_p.BaseModel, extra='forbid'):
    """
    A component that will be replaced by the server with the component returned by the given URL.
    """

    path: str
    load_trigger: _t.Union[events.PageEvent, None] = _p.Field(default=None, serialization_alias='loadTrigger')
    components: '_t.Union[_t.List[AnyComponent], None]' = None
    sse: _t.Union[bool, None] = None
    type: _t.Literal['ServerLoad'] = 'ServerLoad'


class Image(_p.BaseModel, extra='forbid'):
    src: str
    alt: _t.Union[str, None] = None
    width: _t.Union[str, int, None] = None
    height: _t.Union[str, int, None] = None
    referrer_policy: _t.Union[
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
    ] = _p.Field(None, serialization_alias='referrerPolicy')
    loading: _t.Union[_t.Literal['eager', 'lazy'], None] = None
    on_click: _t.Union[events.AnyEvent, None] = _p.Field(default=None, serialization_alias='onClick')
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['Image'] = 'Image'


class Iframe(_p.BaseModel, extra='forbid'):
    src: _p.HttpUrl
    title: _t.Union[str, None] = None
    width: _t.Union[str, int, None] = None
    height: _t.Union[str, int, None] = None
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['Iframe'] = 'Iframe'


class Custom(_p.BaseModel, extra='forbid'):
    data: json_schema.JsonData
    sub_type: str = _p.Field(serialization_alias='subType')
    library: _t.Union[str, None] = None
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['Custom'] = 'Custom'


AnyComponent = _t.Union[
    Text,
    Paragraph,
    PageTitle,
    Div,
    Page,
    Heading,
    Markdown,
    Code,
    Json,
    Button,
    Link,
    LinkList,
    Navbar,
    Modal,
    ServerLoad,
    Image,
    Iframe,
    Custom,
    Table,
    Pagination,
    Display,
    Details,
    Form,
    FormField,
    ModelForm,
]
