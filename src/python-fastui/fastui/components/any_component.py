import typing as _t

import pydantic as _p
import typing_extensions as _te

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
    Link,
    Modal,
    Page,
    ServerLoad,
    Toast,
)
from .display import Details, Display
from .forms import (
    Form,
    FormField,
    ModelForm,
)
from .tables import Pagination, Table

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
