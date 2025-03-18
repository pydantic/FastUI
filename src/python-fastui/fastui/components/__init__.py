"""
Component definitions.

All CamelCase names in the namespace should be components.
"""

from .any_component import AnyComponent
from .basic import (
    Button,
    Code,
    Custom,
    Error,
    FireEvent,
    Footer,
    Heading,
    Iframe,
    Image,
    Json,
    Link,
    LinkList,
    Markdown,
    Navbar,
    PageTitle,
    Paragraph,
    Spinner,
    Text,
    Video,
)
from .containers import (
    Div,
    Modal,
    Page,
    ServerLoad,
    Toast,
)
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
    'Video',
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
    # then the other form field types which are included in `AnyComponent` via the `FormField` union
    'FormFieldBoolean',
    'FormFieldFile',
    'FormFieldInput',
    'FormFieldSelect',
    'FormFieldSelectSearch',
    'AnyComponent',
)
