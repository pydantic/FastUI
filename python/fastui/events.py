from typing import Annotated, Literal

from pydantic import BaseModel, Field


class PageEvent(BaseModel):
    type: Literal['page'] = 'page'
    name: str


class GoToEvent(BaseModel):
    type: Literal['go-to'] = 'go-to'
    # can be a path or a URL
    url: str


Event = Annotated[PageEvent | GoToEvent, Field(discriminator='type')]
