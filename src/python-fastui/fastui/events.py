from typing import Annotated, Literal

from pydantic import Field
from typing_extensions import TypeAliasType

from .base import BaseModel

ContextType = TypeAliasType('ContextType', dict[str, str | int])


class PageEvent(BaseModel, defer_build=True):
    name: str
    push_path: str | None = None
    context: ContextType | None = None
    clear: bool | None = None
    next_event: 'AnyEvent | None' = None
    type: Literal['page'] = 'page'


class GoToEvent(BaseModel):
    # can be a path or a full URL
    url: str | None = None
    query: dict[str, str | float | None] | None = None
    target: Literal['_blank'] | None = None
    type: Literal['go-to'] = 'go-to'


class BackEvent(BaseModel):
    type: Literal['back'] = 'back'


class AuthEvent(BaseModel):
    # False means clear the token and thereby logout the user
    token: str | Literal[False]
    url: str | None = None
    type: Literal['auth'] = 'auth'


AnyEvent = Annotated[PageEvent | GoToEvent | BackEvent | AuthEvent, Field(discriminator='type')]

PageEvent.model_rebuild(_types_namespace={'AnyEvent': AnyEvent})
