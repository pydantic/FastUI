import typing as _t
from abc import ABC

import pydantic as _p
import typing_extensions as _te

from fastui import class_name as _class_name
from fastui import events

from .. import types as _types
from ..base import BaseModel

if _t.TYPE_CHECKING:
    from .any_component import AnyComponent


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


class BaseForm(BaseModel, ABC, defer_build=True, extra='forbid'):
    """Base class for forms."""

    submit_url: str
    """URL to submit the form data to."""

    initial: _t.Union[_t.Dict[str, _types.JsonData], None] = None
    """Initial values for the form fields, mapping field names to values."""

    method: _t.Literal['POST', 'GOTO', 'GET'] = 'POST'
    """HTTP method to use for the form submission."""

    display_mode: _t.Union[_t.Literal['default', 'page', 'inline'], None] = None
    """Display mode for the form."""

    submit_on_change: _t.Union[bool, None] = None
    """Whether to submit the form on change."""

    submit_trigger: _t.Union[events.PageEvent, None] = None
    """Event to trigger form submission."""

    loading: '_t.Union[_t.List[AnyComponent], None]' = None
    """Components to display while the form is submitting."""

    footer: '_t.Union[_t.List[AnyComponent], None]' = None
    """Components to display in the form footer."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the form's HTML component."""

    @_p.model_validator(mode='after')
    def default_footer(self) -> _te.Self:
        if self.footer is None and self.display_mode == 'inline':
            self.footer = []
        return self
