from __future__ import annotations as _annotations

import typing
from abc import ABC

import pydantic

from . import extra

if typing.TYPE_CHECKING:
    from . import AnyComponent

InputHtmlType = typing.Literal['text', 'date', 'datetime-local', 'time', 'email', 'url', 'file', 'number']


class BaseFormField(pydantic.BaseModel, ABC, defer_build=True):
    name: str
    title: str | list[str]
    required: bool = False
    error: str | None = None
    locked: bool = False
    class_name: extra.ClassName | None = None


class FormFieldInput(BaseFormField):
    html_type: InputHtmlType = pydantic.Field(default='text', serialization_alias='htmlType')
    initial: str | int | float | None = None
    type: typing.Literal['FormFieldInput'] = 'FormFieldInput'


class FormFieldCheckbox(BaseFormField):
    initial: bool | None = None
    type: typing.Literal['FormFieldCheckbox'] = 'FormFieldCheckbox'


class FormFieldSelect(BaseFormField):
    choices: list[tuple[str, str]]
    initial: str | None = None
    type: typing.Literal['FormFieldSelect'] = 'FormFieldSelect'


class FormFieldFile(BaseFormField):
    multiple: bool = False
    accept: str | None = None
    type: typing.Literal['FormFieldFile'] = 'FormFieldFile'


FormField = FormFieldInput | FormFieldCheckbox | FormFieldSelect | FormFieldFile


class BaseForm(pydantic.BaseModel, ABC, defer_build=True):
    submit_url: str = pydantic.Field(serialization_alias='submitUrl')
    footer: bool | list[AnyComponent] | None = None
    class_name: extra.ClassName | None = None


class Form(BaseForm):
    form_fields: list[FormField] = pydantic.Field(serialization_alias='formFields')
    type: typing.Literal['Form'] = 'Form'


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
