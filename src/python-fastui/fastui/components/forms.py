import typing as _t
from abc import ABC

import pydantic
import typing_extensions as _te

from .. import class_name as _class_name
from .. import forms

if _t.TYPE_CHECKING:
    from . import AnyComponent

InputHtmlType = _t.Literal['text', 'date', 'datetime-local', 'time', 'email', 'url', 'number', 'password']


class BaseFormField(pydantic.BaseModel, ABC, defer_build=True):
    name: str
    title: _t.Union[str, _t.List[str]]
    required: bool = False
    error: _t.Union[str, None] = None
    locked: bool = False
    description: _t.Union[str, None] = None
    class_name: _class_name.ClassName = None


class FormFieldInput(BaseFormField):
    html_type: InputHtmlType = pydantic.Field(default='text', serialization_alias='htmlType')
    initial: _t.Union[str, int, float, None] = None
    placeholder: _t.Union[str, None] = None
    type: _t.Literal['FormFieldInput'] = 'FormFieldInput'


class FormFieldBoolean(BaseFormField):
    initial: _t.Union[bool, None] = None
    mode: _t.Literal['checkbox', 'switch'] = 'checkbox'
    type: _t.Literal['FormFieldBoolean'] = 'FormFieldBoolean'


class FormFieldFile(BaseFormField):
    multiple: _t.Union[bool, None] = None
    accept: _t.Union[str, None] = None
    type: _t.Literal['FormFieldFile'] = 'FormFieldFile'


class FormFieldSelect(BaseFormField):
    options: _t.Union[_t.List[forms.SelectOption], _t.List[forms.SelectGroup]]
    multiple: _t.Union[bool, None] = None
    initial: _t.Union[str, None] = None
    vanilla: _t.Union[bool, None] = None
    placeholder: _t.Union[str, None] = None
    type: _t.Literal['FormFieldSelect'] = 'FormFieldSelect'


class FormFieldSelectSearch(BaseFormField):
    search_url: str = pydantic.Field(serialization_alias='searchUrl')
    multiple: _t.Union[bool, None] = None
    initial: _t.Union[forms.SelectOption, None] = None
    # time in ms to debounce requests by, defaults to 300ms
    debounce: _t.Union[int, None] = None
    placeholder: _t.Union[str, None] = None
    type: _t.Literal['FormFieldSelectSearch'] = 'FormFieldSelectSearch'


FormField = _t.Union[FormFieldInput, FormFieldBoolean, FormFieldFile, FormFieldSelect, FormFieldSelectSearch]


class BaseForm(pydantic.BaseModel, ABC, defer_build=True, extra='forbid'):
    submit_url: str = pydantic.Field(serialization_alias='submitUrl')
    initial: _t.Union[_t.Dict[str, _t.Any], None] = None
    method: _t.Literal['POST', 'GOTO', 'GET'] = 'POST'
    display_mode: _t.Union[_t.Literal['default', 'inline'], None] = pydantic.Field(
        default=None, serialization_alias='displayMode'
    )
    submit_on_change: _t.Union[bool, None] = pydantic.Field(default=None, serialization_alias='submitOnChange')
    footer: '_t.Union[bool, _t.List[AnyComponent], None]' = None
    class_name: _class_name.ClassName = None

    @pydantic.model_validator(mode='after')
    def default_footer(self) -> _te.Self:
        if self.footer is None and self.display_mode == 'inline':
            self.footer = False
        return self


class Form(BaseForm):
    form_fields: _t.List[FormField] = pydantic.Field(serialization_alias='formFields')
    type: _t.Literal['Form'] = 'Form'


FormFieldsModel = _t.TypeVar('FormFieldsModel', bound=pydantic.BaseModel)


class ModelForm(BaseForm, _t.Generic[FormFieldsModel]):
    #  TODO should we change this to simply have
    # model: type[pydantic.BaseModel] = pydantic.Field(exclude=True)
    type: _t.Literal['ModelForm'] = 'ModelForm'

    @pydantic.computed_field(alias='formFields')
    def form_fields(self) -> _t.List[FormField]:
        from ..json_schema import model_json_schema_to_fields

        args = self.__pydantic_generic_metadata__['args']
        try:
            model: _t.Type[FormFieldsModel] = args[0]
        except IndexError:
            raise ValueError('`ModelForm` must be parameterized with a pydantic model, i.e. `ModelForm[MyModel]()`.')

        if not issubclass(model, pydantic.BaseModel):
            raise TypeError('`ModelForm` must be parameterized with a pydantic model, i.e. `ModelForm[MyModel]()`.')
        return model_json_schema_to_fields(model)
