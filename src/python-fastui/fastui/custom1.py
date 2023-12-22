"""
Example usage a user might use with custom components.

Note that it's not working with discriminator uncommented, which we need to fix, I think that's a bug in Pydantic.

(I got the same issue even if I dropped the TypeAliasType and just used the Union directly.)
"""
import typing as _t

import pydantic as _p
import typing_extensions as _te

import fastui.components as c
from fastui.class_name import ClassNameField
from fastui.types import JsonData


class Custom(_p.BaseModel, extra='forbid'):
    type: _t.Literal['Custom'] = 'Custom'

    data: JsonData
    sub_type: str = _p.Field(serialization_alias='subType')
    library: _t.Union[str, None] = None
    class_name: ClassNameField = None


CustomAnyComponent = _te.TypeAliasType(
    'CustomAnyComponent',
    _te.Annotated[
        _t.Union[
            Custom,
            # Non-recursive components
            c.Text,
            c.Paragraph,
            c.PageTitle,
            c.Heading,
            c.Markdown,
            c.Code,
            c.Json,
            c.Button,
            c.Image,
            c.Iframe,
            c.Video,
            c.FireEvent,
            c.Table,
            c.Pagination,
            c.Display,
            c.Details,
            c.Form,
            c.FormField,
            c.ModelForm,
            # Recursive components
            'c.Div[CustomAnyComponent]',
            'c.Page[CustomAnyComponent]',
            'c.Link[CustomAnyComponent]',
            'c.LinkList[CustomAnyComponent]',
            'c.Modal[CustomAnyComponent]',
            'c.ServerLoad[CustomAnyComponent]',
            'c.Navbar[CustomAnyComponent]',
        ],
        ...,
        # _p.Field(discriminator='type'),
    ],
)


class FastUI(_p.RootModel):
    """
    The root component of a FastUI application.
    """

    root: _t.List[CustomAnyComponent]


print(FastUI.model_json_schema())
