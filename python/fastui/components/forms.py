import typing

import pydantic

from .. import events
from . import extra

FormModel = typing.TypeVar('FormModel', bound=pydantic.BaseModel)


class Form(pydantic.BaseModel, typing.Generic[FormModel]):
    submit_trigger: events.PageEvent | None = pydantic.Field(default=None, serialization_alias='submitTrigger')
    submit_url: str | None = pydantic.Field(default=None, serialization_alias='submitUrl')
    next_url: str | None = pydantic.Field(default=None, serialization_alias='nextUrl')
    class_name: extra.ClassName | None = None
    type: typing.Literal['Form'] = 'Form'

    @pydantic.computed_field(alias='formJsonSchema')
    def form_json_schema(self) -> dict[str, typing.Any]:
        args = self.__pydantic_generic_metadata__['args']
        try:
            model: type[FormModel] = args[0]
        except IndexError:
            raise ValueError('`Form` must be parameterized with a pydantic model, i.e. `Form[MyModel]()`.')

        if not issubclass(model, pydantic.BaseModel):
            raise TypeError('`Form` must be parameterized with a pydantic model, i.e. `Form[MyModel]()`.')
        return model.model_json_schema()
