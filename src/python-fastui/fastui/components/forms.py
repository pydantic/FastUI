from __future__ import annotations as _annotations

import typing
from abc import ABC

import pydantic
import typing_extensions as _te

from .. import class_name as _class_name
from .. import forms

if typing.TYPE_CHECKING:
    from . import AnyComponent

InputHtmlType = typing.Literal['text', 'date', 'datetime-local', 'time', 'email', 'url', 'number', 'password']


class BaseFormField(pydantic.BaseModel, ABC, defer_build=True):
    name: str
    title: typing.Union[str, typing.List[str]]
    required: bool = False
    error: typing.Union[str, None] = None
    locked: bool = False
    description: typing.Union[str, None] = None
    class_name: _class_name.ClassName = None


class FormFieldInput(BaseFormField):
    html_type: InputHtmlType = pydantic.Field(default='text', serialization_alias='htmlType')
    initial: typing.Union[str, int, float, None] = None
    placeholder: typing.Union[str, None] = None
    type: typing.Literal['FormFieldInput'] = 'FormFieldInput'


class FormFieldBoolean(BaseFormField):
    initial: typing.Union[bool, None] = None
    mode: typing.Literal['checkbox', 'switch'] = 'checkbox'
    type: typing.Literal['FormFieldBoolean'] = 'FormFieldBoolean'


class FormFieldFile(BaseFormField):
    multiple: typing.Union[bool, None] = None
    accept: typing.Union[str, None] = None
    type: typing.Literal['FormFieldFile'] = 'FormFieldFile'


class FormFieldSelect(BaseFormField):
    options: typing.Union[typing.List[forms.SelectOption], typing.List[forms.SelectGroup]]
    multiple: typing.Union[bool, None] = None
    initial: typing.Union[str, None] = None
    vanilla: typing.Union[bool, None] = None
    placeholder: typing.Union[str, None] = None
    type: typing.Literal['FormFieldSelect'] = 'FormFieldSelect'


class FormFieldSelectSearch(BaseFormField):
    search_url: str = pydantic.Field(serialization_alias='searchUrl')
    multiple: typing.Union[bool, None] = None
    initial: typing.Union[forms.SelectOption, None] = None
    # time in ms to debounce requests by, defaults to 300ms
    debounce: typing.Union[int, None] = None
    placeholder: typing.Union[str, None] = None
    type: typing.Literal['FormFieldSelectSearch'] = 'FormFieldSelectSearch'


FormField = typing.Union[FormFieldInput, FormFieldBoolean, FormFieldFile, FormFieldSelect, FormFieldSelectSearch]


class BaseForm(pydantic.BaseModel, ABC, defer_build=True, extra='forbid'):
    submit_url: str = pydantic.Field(serialization_alias='submitUrl')
    initial: typing.Union[typing.Dict[str, typing.Any], None] = None
    method: typing.Literal['POST', 'GOTO', 'GET'] = 'POST'
    display_mode: typing.Union[typing.Literal['default', 'inline'], None] = pydantic.Field(
        default=None, serialization_alias='displayMode'
    )
    submit_on_change: typing.Union[bool, None] = pydantic.Field(default=None, serialization_alias='submitOnChange')
    footer: typing.Union[bool, typing.List[AnyComponent], None] = None
    class_name: _class_name.ClassName = None

    @pydantic.model_validator(mode='after')
    def default_footer(self) -> _te.Self:
        if self.footer is None and self.display_mode == 'inline':
            self.footer = False
        return self


class Form(BaseForm):
    form_fields: typing.List[FormField] = pydantic.Field(serialization_alias='formFields')
    type: typing.Literal['Form'] = 'Form'


FormFieldsModel = typing.TypeVar('FormFieldsModel', bound=pydantic.BaseModel)


class ModelForm(BaseForm, typing.Generic[FormFieldsModel]):
    #  TODO should we change this to simply have
    # model: type[pydantic.BaseModel] = pydantic.Field(exclude=True)
    type: typing.Literal['ModelForm'] = 'ModelForm'

    @pydantic.computed_field(alias='formFields')
    def form_fields(self) -> typing.List[FormField]:
        from ..json_schema import model_json_schema_to_fields

        args = self.__pydantic_generic_metadata__['args']
        try:
            model: type[FormFieldsModel] = args[0]
        except IndexError:
            raise ValueError('`ModelForm` must be parameterized with a pydantic model, i.e. `ModelForm[MyModel]()`.')

        if not issubclass(model, pydantic.BaseModel):
            raise TypeError('`ModelForm` must be parameterized with a pydantic model, i.e. `ModelForm[MyModel]()`.')
        return model_json_schema_to_fields(model)
