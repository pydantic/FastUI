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
    title: str
    variant: Union[Literal['normal', 'action', 'success', 'info', 'warning', 'error', 'loading'], None] = None
    invert: Union[bool, None] = None
    dismissible: Union[bool, None] = None
    description: Union[str, None] = None
    duration: Union[int, None] = None
    position: Union[
        Literal['top-left', 'top-right', 'bottom-left', 'bottom-right', 'top-center', 'bottom-center'], None
    ] = None


AnyEvent = Annotated[Union[PageEvent, GoToEvent, BackEvent, ToastEvent], Field(discriminator='type')]
