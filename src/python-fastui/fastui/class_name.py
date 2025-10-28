# could be renamed to something general if there's more to add
from typing import Annotated, Literal

from pydantic import Field
from typing_extensions import TypeAliasType

ClassName = TypeAliasType('ClassName', str | list['ClassName'] | dict[str, bool | None] | None)
ClassNameField = Annotated[ClassName, Field(serialization_alias='className')]

NamedStyle = TypeAliasType('NamedStyle', Literal['primary', 'secondary', 'warning'] | None)
NamedStyleField = Annotated[NamedStyle, Field(serialization_alias='namedStyle')]
