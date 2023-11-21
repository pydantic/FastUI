from typing import Annotated, Literal

from pydantic import BaseModel, Field


class PageEvent(BaseModel):
    name: str
    type: Literal['page'] = 'page'


class GoToEvent(BaseModel):
    # can be a path or a full URL
    url: str
    type: Literal['go-to'] = 'go-to'


class BackEvent(BaseModel):
    type: Literal['back'] = 'back'


Event = Annotated[PageEvent | GoToEvent | BackEvent, Field(discriminator='type')]
