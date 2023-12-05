# could be renamed to something general if there's more to add
from typing import Dict, List, Union

from pydantic import Field
from typing_extensions import Annotated

ClassName = Annotated[Union[str, List[str], Dict[str, Union[bool, None]], None], Field(serialization_alias='className')]
