from typing import Annotated, Literal

from pydantic import BaseModel, Field


class PageEvent(BaseModel):
    name: str
    type: Literal['page'] = 'page'


class GoToEvent(BaseModel):
    # can be a path or a full URL
    url: str
    type: Literal['go-to'] = 'go-to'


Event = Annotated[PageEvent | GoToEvent, Field(discriminator='type')]
