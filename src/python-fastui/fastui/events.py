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


AnyEvent = Annotated[Union[PageEvent, GoToEvent, BackEvent], Field(discriminator='type')]
