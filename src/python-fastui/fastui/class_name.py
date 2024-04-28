# could be renamed to something general if there's more to add
from typing import Dict, List, Literal, Union

from typing_extensions import Annotated, TypeAliasType

from pydantic import Field

ClassName = TypeAliasType('ClassName', Union[str, List['ClassName'], Dict[str, Union[bool, None]], None])
ClassNameField = Annotated[ClassName, Field(serialization_alias='className')]

NamedStyle = TypeAliasType('NamedStyle', Union[Literal['primary', 'secondary', 'warning'], None])
NamedStyleField = Annotated[NamedStyle, Field(serialization_alias='namedStyle')]
