"""
Component definitions.

All CamelCase names in the namespace should be components.
"""
import typing as _t

import pydantic as _p
import typing_extensions as _te
from pydantic_core import core_schema as _core_schema

from .. import class_name as _class_name
from .. import events
from .. import types as _types
from ..base import BaseModel
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
    # first we include all components from this file
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
    'FireEvent',
    'Error',
    'Spinner',
    'Toast',
    'Custom',
    # then we include components from other files
    'Table',
    'Pagination',
    'Display',
    'Details',
    'Form',
    'FormField',
    'ModelForm',
    'Footer',
    # then `AnyComponent` itself
    'AnyComponent',
    # then the other form field types which are included in `AnyComponent` via the `FormField` union
    'FormFieldBoolean',
    'FormFieldFile',
    'FormFieldInput',
    'FormFieldSelect',
    'FormFieldSelectSearch',
)


class Text(BaseModel, extra='forbid'):
    """Text component that displays a string."""

    text: str
    """The text to display."""

    type: _t.Literal['Text'] = 'Text'
    """The type of the component. Always 'Text'."""


class Paragraph(BaseModel, extra='forbid'):
    """Paragraph component that displays a string as a paragraph."""

    text: str
    """The text to display."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the paragraph's HTML component."""

    type: _t.Literal['Paragraph'] = 'Paragraph'
    """The type of the component. Always 'Paragraph'."""


class PageTitle(BaseModel, extra='forbid'):
    """Sets the title of the HTML page via the `document.title` property."""

    text: str
    """The text to set as the page title."""

    type: _t.Literal['PageTitle'] = 'PageTitle'
    """The type of the component. Always 'PageTitle'."""


class Div(BaseModel, extra='forbid'):
    """A generic container component."""

    components: '_t.List[AnyComponent]'
    """List of components to render inside the div."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the div's HTML component."""

    type: _t.Literal['Div'] = 'Div'
    """The type of the component. Always 'Div'."""


class Page(BaseModel, extra='forbid'):
    """Similar to `container` in many UI frameworks, this acts as a root component for most pages."""

    components: '_t.List[AnyComponent]'
    """List of components to render on the page."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the page's HTML component."""

    type: _t.Literal['Page'] = 'Page'
    """The type of the component. Always 'Page'."""


class Heading(BaseModel, extra='forbid'):
    """Heading component."""

    text: str
    """The text to display in the heading."""

    level: _t.Literal[1, 2, 3, 4, 5, 6] = 1
    """The level of the heading. 1 is the largest, 6 is the smallest."""

    html_id: _t.Union[str, None] = None
    """Optional HTML ID to apply to the heading's HTML component."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the page's HTML component."""

    type: _t.Literal['Heading'] = 'Heading'
    """The type of the component. Always 'Heading'."""

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: _core_schema.CoreSchema, handler: _p.GetJsonSchemaHandler
    ) -> _t.Any:
        # until https://github.com/pydantic/pydantic/issues/8413 is fixed
        json_schema = handler(core_schema)
        json_schema['required'].append('level')
        return json_schema


CodeStyle = _te.Annotated[_t.Union[str, None], _p.Field(serialization_alias='codeStyle')]
"""
Code style to apply to a `Code` component.

Attributes:
    codeStyle: The code style to apply. If None, no style is applied.

See Also:
    - [PrismJS Themes](https://github.com/PrismJS/prism-themes)
    - [PrismJS Theme Index](https://cdn.jsdelivr.net/npm/react-syntax-highlighter@15.5.0/dist/esm/styles/prism/index.js)
"""


class Markdown(BaseModel, extra='forbid'):
    """Markdown component that renders markdown text."""

    text: str
    """The markdown text to render."""

    code_style: CodeStyle = None
    """Optional code style to apply to the markdown text."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the page's HTML component."""

    type: _t.Literal['Markdown'] = 'Markdown'
    """The type of the component. Always 'Markdown'."""


class Code(BaseModel, extra='forbid'):
    """Code component that renders code with syntax highlighting."""

    text: str
    """The code to render."""

    language: _t.Union[str, None] = None
    """Optional language of the code. If None, no syntax highlighting is applied."""

    code_style: CodeStyle = None
    """Optional code style to apply to the code."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the page's HTML component."""

    type: _t.Literal['Code'] = 'Code'
    """The type of the component. Always 'Code'."""


class Json(BaseModel, extra='forbid'):
    """JSON component that renders JSON data."""

    value: _types.JsonData
    """The JSON data to render."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the page's HTML component."""

    type: _t.Literal['JSON'] = 'JSON'
    """The type of the component. Always 'JSON'."""


class Button(BaseModel, extra='forbid'):
    """Button component."""

    text: str
    """The text to display on the button."""

    on_click: _t.Union[events.AnyEvent, None] = None
    """Optional event to trigger when the button is clicked."""

    html_type: _t.Union[_t.Literal['button', 'reset', 'submit'], None] = None
    """Optional HTML type of the button. If None, defaults to 'button'."""

    named_style: _class_name.NamedStyleField = None
    """Optional named style to apply to the button."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the button's HTML component."""

    type: _t.Literal['Button'] = 'Button'
    """The type of the component. Always 'Button'."""


class Link(BaseModel, extra='forbid'):
    """Link component."""

    components: '_t.List[AnyComponent]'
    """List of components to render attached to the link."""

    on_click: _t.Union[events.AnyEvent, None] = None
    """Optional event to trigger when the link is clicked."""

    mode: _t.Union[_t.Literal['navbar', 'footer', 'tabs', 'vertical', 'pagination'], None] = None
    """Optional mode of the link."""

    active: _t.Union[str, bool, None] = None
    """Optional active state of the link."""

    locked: _t.Union[bool, None] = None
    """Optional locked state of the link."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the link's HTML component."""

    type: _t.Literal['Link'] = 'Link'
    """The type of the component. Always 'Link'."""


class LinkList(BaseModel, extra='forbid'):
    """List of Link components."""

    links: _t.List[Link]
    """List of links to render."""

    mode: _t.Union[_t.Literal['tabs', 'vertical', 'pagination'], None] = None
    """Optional mode of the link list."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the link list's HTML component."""

    type: _t.Literal['LinkList'] = 'LinkList'
    """The type of the component. Always 'LinkList'."""


class Navbar(BaseModel, extra='forbid'):
    """Navbar component used for moving between pages."""

    title: _t.Union[str, None] = None
    """Optional title to display in the navbar."""

    title_event: _t.Union[events.AnyEvent, None] = None
    """Optional event to trigger when the title is clicked. Often used to navigate to the home page."""

    start_links: _t.List[Link] = []
    """List of links to render at the start of the navbar."""

    end_links: _t.List[Link] = []
    """List of links to render at the end of the navbar."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the navbar's HTML component."""

    type: _t.Literal['Navbar'] = 'Navbar'
    """The type of the component. Always 'Navbar'."""

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: _core_schema.CoreSchema, handler: _p.GetJsonSchemaHandler
    ) -> _t.Any:
        # until https://github.com/pydantic/pydantic/issues/8413 is fixed
        json_schema = handler(core_schema)
        json_schema.setdefault('required', []).extend(['startLinks', 'endLinks'])
        return json_schema


class Footer(BaseModel, extra='forbid'):
    """Footer component."""

    links: _t.List[Link]
    """List of links to render in the footer."""

    extra_text: _t.Union[str, None] = None
    """Optional extra text to display in the footer."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the footer's HTML component."""

    type: _t.Literal['Footer'] = 'Footer'
    """The type of the component. Always 'Footer'."""


class Modal(BaseModel, extra='forbid'):
    """Modal component that displays a modal dialog."""

    title: str
    """The text displayed on the modal trigger button."""

    body: '_t.List[AnyComponent]'
    """List of components to render in the modal body."""

    footer: '_t.Union[_t.List[AnyComponent], None]' = None
    """Optional list of components to render in the modal footer."""

    open_trigger: _t.Union[events.PageEvent, None] = None
    """Optional event to trigger when the modal is opened."""

    open_context: _t.Union[events.ContextType, None] = None
    """Optional context to pass to the open trigger event."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the modal's HTML component."""

    type: _t.Literal['Modal'] = 'Modal'
    """The type of the component. Always 'Modal'."""


class ServerLoad(BaseModel, extra='forbid'):
    """A component that will be replaced by the server with the component returned by the given URL."""

    path: str
    """The URL to load the component from."""

    load_trigger: _t.Union[events.PageEvent, None] = None
    """Optional event to trigger when the component is loaded."""

    components: '_t.Union[_t.List[AnyComponent], None]' = None
    """Optional list of components to render while the server is loading the new component(s)."""

    sse: _t.Union[bool, None] = None
    """Optional flag to enable server-sent events (SSE) for the server load."""

    sse_retry: _t.Union[int, None] = None
    """Optional time in milliseconds to retry the SSE connection."""

    method: _t.Union[_t.Literal['GET', 'POST', 'PATCH', 'PUT', 'DELETE'], None] = None
    """Optional HTTP method to use when loading the component."""

    type: _t.Literal['ServerLoad'] = 'ServerLoad'
    """The type of the component. Always 'ServerLoad'."""


class Image(BaseModel, extra='forbid'):
    """Image container component."""

    src: str
    """The URL of the image to display."""

    alt: _t.Union[str, None] = None
    """Optional alt text for the image."""

    width: _t.Union[str, int, None] = None
    """Optional width used to display the image."""

    height: _t.Union[str, int, None] = None
    """Optional height used to display the image."""

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
    ] = None
    """Optional referrer policy for the image. Specifies what information to send when fetching the image.

    For more info, see https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy."""

    loading: _t.Union[_t.Literal['eager', 'lazy'], None] = None
    """Optional loading strategy for the image."""

    on_click: _t.Union[events.AnyEvent, None] = None
    """Optional event to trigger when the image is clicked."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the image's HTML component."""

    type: _t.Literal['Image'] = 'Image'
    """The type of the component. Always 'Image'."""


class Iframe(BaseModel, extra='forbid'):
    """Iframe component that displays content from a URL."""

    src: _p.HttpUrl
    """The URL of the content to display."""

    title: _t.Union[str, None] = None
    """Optional title for the iframe."""

    width: _t.Union[str, int, None] = None
    """Optional width used to display the iframe."""

    height: _t.Union[str, int, None] = None
    """Optional height used to display the iframe."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the iframe's HTML component."""

    srcdoc: _t.Union[str, None] = None
    """Optional HTML content to display in the iframe."""

    sandbox: _t.Union[str, None] = None
    """Optional sandbox policy for the iframe. Specifies restrictions on the HTML content in the iframe."""

    type: _t.Literal['Iframe'] = 'Iframe'
    """The type of the component. Always 'Iframe'."""


class Video(BaseModel, extra='forbid'):
    """Video component that displays a video or multiple videos."""

    sources: _t.List[_p.AnyUrl]
    """List of URLs to the video sources."""

    autoplay: _t.Union[bool, None] = None
    """Optional flag to enable autoplay for the video."""

    controls: _t.Union[bool, None] = None
    """Optional flag to enable controls (pause, play, etc) for the video."""

    loop: _t.Union[bool, None] = None
    """Optional flag to enable looping for the video."""

    muted: _t.Union[bool, None] = None
    """Optional flag to mute the video."""

    poster: _t.Union[_p.AnyUrl, None] = None
    """Optional URL to an image to display as the video poster (what is shown when the video is loading or until the user plays it)."""

    width: _t.Union[str, int, None] = None
    """Optional width used to display the video."""

    height: _t.Union[str, int, None] = None
    """Optional height used to display the video."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the video's HTML component."""

    type: _t.Literal['Video'] = 'Video'
    """The type of the component. Always 'Video'."""


class FireEvent(BaseModel, extra='forbid'):
    """Fire an event."""

    event: events.AnyEvent
    """The event to fire."""

    message: _t.Union[str, None] = None
    """Optional message to display when the event is fired. Defaults to a blank message."""

    type: _t.Literal['FireEvent'] = 'FireEvent'
    """The type of the component. Always 'FireEvent'."""


class Error(BaseModel, extra='forbid'):
    """Utility component used to display an error."""

    title: str
    """The title of the error."""

    description: str
    """The description of the error."""

    status_code: _t.Union[int, None] = None
    """Optional status code of the error."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the error's HTML component."""

    type: _t.Literal['Error'] = 'Error'
    """The type of the component. Always 'Error'."""

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: _core_schema.CoreSchema, handler: _p.GetJsonSchemaHandler
    ) -> _t.Any:
        # add `children` to the schema so it can be used in the client
        json_schema = handler(core_schema)
        json_schema['properties']['children'] = {'tsType': 'ReactNode'}
        return json_schema


class Spinner(BaseModel, extra='forbid'):
    """Spinner component that displays a loading spinner."""

    text: _t.Union[str, None] = None
    """Optional text to display with the spinner."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the spinner's HTML component."""

    type: _t.Literal['Spinner'] = 'Spinner'
    """The type of the component. Always 'Spinner'."""


class Toast(BaseModel, extra='forbid'):
    """Toast component that displays a toast message (small temporary message)."""

    title: str
    """The title of the toast."""

    body: '_t.List[AnyComponent]'
    """List of components to render in the toast body."""

    # TODO: change these before the release (top left, center, end, etc). Can be done with the toast bug fix.
    position: _t.Union[
        _t.Literal[
            'top-start',
            'top-center',
            'top-end',
            'middle-start',
            'middle-center',
            'middle-end',
            'bottom-start',
            'bottom-center',
            'bottom-end',
        ],
        None,
    ] = None
    """Optional position of the toast."""

    open_trigger: _t.Union[events.PageEvent, None] = None
    """Optional event to trigger when the toast is opened."""

    open_context: _t.Union[events.ContextType, None] = None
    """Optional context to pass to the open trigger event."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the toast's HTML component."""

    type: _t.Literal['Toast'] = 'Toast'
    """The type of the component. Always 'Toast'."""


class Custom(BaseModel, extra='forbid'):
    """Custom component that allows for special data to be rendered."""

    data: _types.JsonData
    """The data to render in the custom component."""

    sub_type: str
    """The sub-type of the custom component."""

    library: _t.Union[str, None] = None
    """Optional library to use for the custom component."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the custom component's HTML component."""

    type: _t.Literal['Custom'] = 'Custom'
    """The type of the component. Always 'Custom'."""


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
        Json,
        Button,
        Link,
        LinkList,
        Navbar,
        Footer,
        Modal,
        ServerLoad,
        Image,
        Iframe,
        Video,
        FireEvent,
        Error,
        Spinner,
        Custom,
        Table,
        Pagination,
        Display,
        Details,
        Form,
        FormField,
        ModelForm,
        Toast,
    ],
    _p.Field(discriminator='type'),
]
"""Union of all components.

Pydantic discriminator field is set to 'type' to allow for efficient serialization and deserialization of the components."""
