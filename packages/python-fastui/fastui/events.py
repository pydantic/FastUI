from typing import Annotated, Literal, TypeAlias

from pydantic import BaseModel, Field

EventContext: TypeAlias = dict[str, str | int]


class PageEvent(BaseModel):
    name: str
    push_path: str | None = Field(default=None, serialization_alias='pushPath')
    context: EventContext | None = None
    clear: bool | None = None
    type: Literal['page'] = 'page'


class GoToEvent(BaseModel):
    # can be a path or a full URL
    url: str | None = None
    query: dict[str, str | float | None] | None = None
    type: Literal['go-to'] = 'go-to'


class BackEvent(BaseModel):
    type: Literal['back'] = 'back'


AnyEvent = Annotated[PageEvent | GoToEvent | BackEvent, Field(discriminator='type')]
