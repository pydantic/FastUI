from typing import Annotated, Literal

from pydantic import BaseModel, Field


class PageEvent(BaseModel):
    name: str
    push_path: str | None = Field(default=None, serialization_alias='pushPath')
    type: Literal['page'] = 'page'


class GoToEvent(BaseModel):
    # can be a path or a full URL
    url: str
    type: Literal['go-to'] = 'go-to'


class BackEvent(BaseModel):
    type: Literal['back'] = 'back'


AnyEvent = Annotated[PageEvent | GoToEvent | BackEvent, Field(discriminator='type')]
