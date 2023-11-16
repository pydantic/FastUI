import typing
from abc import ABC

import pydantic

from . import extra

HtmlType = typing.Literal['checkbox', 'text', 'date', 'datetime-local', 'time', 'email', 'url', 'file', 'number']


class FormField(pydantic.BaseModel):
    name: str
    title: list[str]
    html_type: HtmlType = pydantic.Field(default='text', serialization_alias='htmlType')
    required: bool = False
    initial: str | int | float | bool | None = None
    class_name: extra.ClassName | None = None
    type: typing.Literal['FormField'] = 'FormField'


class BaseForm(pydantic.BaseModel, ABC):
    submit_url: str = pydantic.Field(serialization_alias='submitUrl')
    class_name: extra.ClassName | None = None


FormFieldsModel = typing.TypeVar('FormFieldsModel', bound=pydantic.BaseModel)


class ModelForm(BaseForm, typing.Generic[FormFieldsModel]):
    type: typing.Literal['ModelForm'] = 'ModelForm'

    @pydantic.computed_field(alias='formFields')
    def form_fields(self) -> list[FormField]:
        from ..json_schema import model_json_schema_to_fields

        args = self.__pydantic_generic_metadata__['args']
        try:
            model: type[FormFieldsModel] = args[0]
        except IndexError:
            raise ValueError('`ModelForm` must be parameterized with a pydantic model, i.e. `ModelForm[MyModel]()`.')

        if not issubclass(model, pydantic.BaseModel):
            raise TypeError('`ModelForm` must be parameterized with a pydantic model, i.e. `ModelForm[MyModel]()`.')
        return model_json_schema_to_fields(model)


class Form(BaseForm):
    form_fields: list[FormField] = pydantic.Field(serialization_alias='formFields')
    type: typing.Literal['Form'] = 'Form'
