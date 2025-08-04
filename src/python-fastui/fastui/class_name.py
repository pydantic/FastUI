# could be renamed to something general if there's more to add
from typing import Annotated, Literal, Union

from pydantic import Field
from typing_extensions import TypeAliasType

ClassName = TypeAliasType('ClassName', Union[str, list['ClassName'], dict[str, Union[bool, None]], None])
ClassNameField = Annotated[ClassName, Field(serialization_alias='className')]

NamedStyle = TypeAliasType('NamedStyle', Union[Literal['primary', 'secondary', 'warning'], None])
NamedStyleField = Annotated[NamedStyle, Field(serialization_alias='namedStyle')]
