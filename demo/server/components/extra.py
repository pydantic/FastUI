from typing import Annotated
from pydantic import Field

ClassName = Annotated[str | list[str] | dict[str, bool | None], Field(serialization_alias='className')]

Trigger = Annotated[str, Field(pattern='^trigger:.*$', max_length=63)]
Url = Annotated[str, Field(pattern=r'^(http|/|\.).*$')]
