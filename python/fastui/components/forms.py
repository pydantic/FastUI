import typing

import pydantic

from .. import events
from . import extra

FormModel = typing.TypeVar('FormModel', bound=pydantic.BaseModel)


class FormHelp(pydantic.BaseModel):
    text: str
    class_name: extra.ClassName | None = None


class FormError(pydantic.BaseModel):
    text: str
    class_name: extra.ClassName | None = None


class Form(pydantic.BaseModel, typing.Generic[FormModel]):
    submit_trigger: events.PageEvent | None = pydantic.Field(default=None, serialization_alias='submitTrigger')
    submit_url: str | None = pydantic.Field(default=None, serialization_alias='submitUrl')
    next_url: str | None = pydantic.Field(default=None, serialization_alias='nextUrl')
    title: str | None = pydantic.Field(default=None, exclude=True)
    help: dict[str, FormHelp] | None = None
    errors: dict[str, FormError] | None = None
    class_name: extra.ClassName | None = None
    type_: typing.Literal['Form'] = pydantic.Field('Form', serialization_alias='type')

    @pydantic.computed_field()
    def form_json_schema(self) -> dict[str, typing.Any]:
        args = self.__pydantic_generic_metadata__['args']
        try:
            model: type[FormModel] = args[0]
        except IndexError:
            raise ValueError('`Form` must be parameterized with a pydantic model, i.e. `Form[MyModel]()`.')

        if not issubclass(model, pydantic.BaseModel):
            raise TypeError('`Form` must be parameterized with a pydantic model, i.e. `Form[MyModel]()`.')
        form_schema = model.model_json_schema()
        if self.title is not None:
            form_schema['title'] = self.title
        return form_schema
