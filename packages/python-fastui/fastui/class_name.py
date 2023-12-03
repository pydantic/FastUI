# could be renamed to something general if there's more to add
from typing import Annotated

from pydantic import Field

ClassName = Annotated[str | list[str] | dict[str, bool | None] | None, Field(serialization_alias='className')]
