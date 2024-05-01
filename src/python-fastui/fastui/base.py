from pydantic import AliasGenerator, ConfigDict
from pydantic import BaseModel as _BaseModel
from pydantic.alias_generators import to_camel


class BaseModel(_BaseModel):
    model_config = ConfigDict(alias_generator=AliasGenerator(serialization_alias=to_camel))
