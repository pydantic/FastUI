from typing import Dict, Literal, Union

from pydantic import BaseModel, Field
from typing_extensions import Annotated, TypeAliasType

ContextType = TypeAliasType('ContextType', Dict[str, Union[str, int]])


class PageEvent(BaseModel):
    name: str
    push_path: Union[str, None] = Field(default=None, serialization_alias='pushPath')
    context: Union[ContextType, None] = None
    clear: Union[bool, None] = None
    type: Literal['page'] = 'page'


class GoToEvent(BaseModel):
    # can be a path or a full URL
    url: Union[str, None] = None
    query: Union[Dict[str, Union[str, float, None]], None] = None
    type: Literal['go-to'] = 'go-to'


class BackEvent(BaseModel):
    type: Literal['back'] = 'back'


class ToastEvent(BaseModel):
    type: Literal['toast'] = 'toast'
    title: str = Field(..., description='Title of the toast.')
    variant: Union[Literal['normal', 'success', 'info', 'warning', 'error'], None] = Field(
        None, description='Variant of the toast.'
    )
    invert: Union[bool, None] = Field(None, description='Dark toast in light mode and vice versa.')
    dismissible: Union[bool, None] = Field(
        None, description="If false, it'll prevent the user from dismissing the toast."
    )
    description: Union[str, None] = Field(None, description="Toast's description, renders underneath the title.")
    duration: Union[int, None] = Field(
        None, description='Time in milliseconds that should elapse before automatically closing the toast.'
    )
    position: Union[
        Literal['top-left', 'top-right', 'bottom-left', 'bottom-right', 'top-center', 'bottom-center'], None
    ] = Field(None, description='Position of the toast.')


AnyEvent = Annotated[Union[PageEvent, GoToEvent, BackEvent, ToastEvent], Field(discriminator='type')]
