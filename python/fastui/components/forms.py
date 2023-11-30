from __future__ import annotations as _annotations

import typing
from abc import ABC

import pydantic

from .. import class_name as _class_name
from .. import forms

if typing.TYPE_CHECKING:
    from . import AnyComponent

InputHtmlType = typing.Literal['text', 'date', 'datetime-local', 'time', 'email', 'url', 'number', 'password']


class BaseFormField(pydantic.BaseModel, ABC, defer_build=True):
    name: str
    title: str | list[str]
    required: bool = False
    error: str | None = None
    locked: bool = False
    description: str | None = None
    class_name: _class_name.ClassName = None


class FormFieldInput(BaseFormField):
    html_type: InputHtmlType = pydantic.Field(default='text', serialization_alias='htmlType')
    initial: str | int | float | None = None
    placeholder: str | None = None
    type: typing.Literal['FormFieldInput'] = 'FormFieldInput'


class FormFieldCheckbox(BaseFormField):
    initial: bool | None = None
    type: typing.Literal['FormFieldCheckbox'] = 'FormFieldCheckbox'


class FormFieldFile(BaseFormField):
    multiple: bool | None = None
    accept: str | None = None
    type: typing.Literal['FormFieldFile'] = 'FormFieldFile'


class FormFieldSelect(BaseFormField):
    options: list[forms.SelectOption] | list[forms.SelectGroup]
    multiple: bool | None = None
    initial: str | None = None
    vanilla: bool | None = None
    placeholder: str | None = None
    type: typing.Literal['FormFieldSelect'] = 'FormFieldSelect'


class FormFieldSelectSearch(BaseFormField):
    search_url: str = pydantic.Field(serialization_alias='searchUrl')
    multiple: bool | None = None
    initial: forms.SelectOption | None = None
    # time in ms to debounce requests by, defaults to 300ms
    debounce: int | None = None
    placeholder: str | None = None
    type: typing.Literal['FormFieldSelectSearch'] = 'FormFieldSelectSearch'


FormField = FormFieldInput | FormFieldCheckbox | FormFieldFile | FormFieldSelect | FormFieldSelectSearch


class BaseForm(pydantic.BaseModel, ABC, defer_build=True):
    submit_url: str = pydantic.Field(serialization_alias='submitUrl')
    initial: dict[str, typing.Any] | None = None
    method: typing.Literal['POST', 'GOTO', 'GET'] = 'POST'
    display_mode: typing.Literal['default', 'inline'] | None = pydantic.Field(
        default=None, serialization_alias='displayMode'
    )
    submit_on_change: bool | None = pydantic.Field(default=None, serialization_alias='submitOnChange')
    footer: bool | list[AnyComponent] | None = None
    class_name: _class_name.ClassName = None

    @pydantic.model_validator(mode='after')
    def default_footer(self) -> typing.Self:
        if self.footer is None and self.display_mode == 'inline':
            self.footer = False
        return self


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
