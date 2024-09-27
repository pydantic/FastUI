from typing import Dict, Literal, Union

from pydantic import Field
from typing_extensions import Annotated, TypeAliasType

from .base import BaseModel

ContextType = TypeAliasType('ContextType', Dict[str, Union[str, int]])


class PageEvent(BaseModel):
    name: str
    push_path: Union[str, None] = None
    context: Union[ContextType, None] = None
    clear: Union[bool, None] = None
    next_event: 'Union[AnyEvent, None]' = None
    type: Literal['page'] = 'page'


class GoToEvent(BaseModel):
    # can be a path or a full URL
    url: Union[str, None] = None
    query: Union[Dict[str, Union[str, float, None]], None] = None
    target: Union[Literal['_blank'], None] = None
    type: Literal['go-to'] = 'go-to'


class BackEvent(BaseModel):
    type: Literal['back'] = 'back'


class AuthEvent(BaseModel):
    # False means clear the token and thereby logout the user
    token: Union[str, Literal[False]]
    url: Union[str, None] = None
    type: Literal['auth'] = 'auth'


AnyEvent = Annotated[Union[PageEvent, GoToEvent, BackEvent, AuthEvent], Field(discriminator='type')]
