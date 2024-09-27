import typing as _t
from abc import ABC

import pydantic
import typing_extensions as _te

from .. import class_name as _class_name
from .. import events, forms
from .. import types as _types
from ..base import BaseModel

if _t.TYPE_CHECKING:
    from . import AnyComponent

InputHtmlType = _t.Literal['text', 'date', 'datetime-local', 'time', 'email', 'url', 'number', 'password', 'hidden']


class BaseFormField(BaseModel, ABC, defer_build=True):
    """Base class for form fields."""

    name: str
    """Name of the field."""

    title: _t.Union[_t.List[str], str]
    """Title of the field to display. Can be a list of strings for multi-line titles."""

    required: bool = False
    """Whether the field is required. Defaults to False."""

    error: _t.Union[str, None] = None
    """Error message to display if the field is invalid."""

    locked: bool = False
    """Whether the field is locked. Defaults to False."""

    description: _t.Union[str, None] = None
    """Description of the field."""

    display_mode: _t.Union[_t.Literal['default', 'inline'], None] = None
    """Display mode for the field."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the field's HTML component."""


class FormFieldInput(BaseFormField):
    """Form field for basic input."""

    html_type: InputHtmlType = 'text'
    """HTML input type for the field."""

    initial: _t.Union[str, float, None] = None
    """Initial value for the field."""

    placeholder: _t.Union[str, None] = None
    """Placeholder text for the field."""

    autocomplete: _t.Union[str, None] = None
    """Autocomplete value for the field."""

    type: _t.Literal['FormFieldInput'] = 'FormFieldInput'
    """The type of the component. Always 'FormFieldInput'."""


class FormFieldTextarea(BaseFormField):
    """Form field for text area input."""

    rows: _t.Union[int, None] = None
    """Number of rows for the text area."""

    cols: _t.Union[int, None] = None
    """Number of columns for the text area."""

    initial: _t.Union[str, None] = None
    """Initial value for the text area."""

    placeholder: _t.Union[str, None] = None
    """Placeholder text for the text area."""

    autocomplete: _t.Union[str, None] = None
    """Autocomplete value for the text area."""

    type: _t.Literal['FormFieldTextarea'] = 'FormFieldTextarea'
    """The type of the component. Always 'FormFieldTextarea'."""


class FormFieldBoolean(BaseFormField):
    """Form field for boolean input."""

    initial: _t.Union[bool, None] = None
    """Initial value for the field."""

    mode: _t.Literal['checkbox', 'switch'] = 'checkbox'
    """Mode for the boolean field."""

    type: _t.Literal['FormFieldBoolean'] = 'FormFieldBoolean'
    """The type of the component. Always 'FormFieldBoolean'."""


class FormFieldFile(BaseFormField):
    """Form field for file input."""

    multiple: _t.Union[bool, None] = None
    """Whether multiple files can be selected."""

    accept: _t.Union[str, None] = None
    """Accepted file types."""

    type: _t.Literal['FormFieldFile'] = 'FormFieldFile'
    """The type of the component. Always 'FormFieldFile'."""


class FormFieldSelect(BaseFormField):
    """Form field for select input."""

    options: forms.SelectOptions
    """Options for the select field."""

    multiple: _t.Union[bool, None] = None
    """Whether multiple options can be selected."""

    initial: _t.Union[_t.List[str], str, None] = None
    """Initial value for the field."""

    vanilla: _t.Union[bool, None] = None
    """Whether to use a vanilla (plain) select element."""

    placeholder: _t.Union[str, None] = None
    """Placeholder text for the field."""

    autocomplete: _t.Union[str, None] = None
    """Autocomplete value for the field."""

    type: _t.Literal['FormFieldSelect'] = 'FormFieldSelect'
    """The type of the component. Always 'FormFieldSelect'."""


class FormFieldSelectSearch(BaseFormField):
    """Form field for searchable select input."""

    search_url: str
    """URL to search for options."""

    multiple: _t.Union[bool, None] = None
    """Whether multiple options can be selected."""

    initial: _t.Union[forms.SelectOption, None] = None
    """Initial value for the field."""

    debounce: _t.Union[int, None] = None
    """Time in milliseconds to debounce requests by. Defaults to 300ms."""

    placeholder: _t.Union[str, None] = None
    """Placeholder text for the field."""

    type: _t.Literal['FormFieldSelectSearch'] = 'FormFieldSelectSearch'
    """The type of the component. Always 'FormFieldSelectSearch'."""


FormField = _t.Union[
    FormFieldInput, FormFieldTextarea, FormFieldBoolean, FormFieldFile, FormFieldSelect, FormFieldSelectSearch
]
"""Union of all form field types."""


class BaseForm(BaseModel, ABC, defer_build=True, extra='forbid'):
    """Base class for forms."""

    submit_url: str
    """URL to submit the form data to."""

    initial: _t.Union[_t.Dict[str, _types.JsonData], None] = None
    """Initial values for the form fields, mapping field names to values."""

    method: _t.Literal['POST', 'GOTO', 'GET'] = 'POST'
    """HTTP method to use for the form submission."""

    display_mode: _t.Union[_t.Literal['default', 'page', 'inline'], None] = None
    """Display mode for the form."""

    submit_on_change: _t.Union[bool, None] = None
    """Whether to submit the form on change."""

    submit_trigger: _t.Union[events.PageEvent, None] = None
    """Event to trigger form submission."""

    loading: '_t.Union[_t.List[AnyComponent], None]' = None
    """Components to display while the form is submitting."""

    footer: '_t.Union[_t.List[AnyComponent], None]' = None
    """Components to display in the form footer."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the form's HTML component."""

    @pydantic.model_validator(mode='after')
    def default_footer(self) -> _te.Self:
        if self.footer is None and self.display_mode == 'inline':
            self.footer = []
        return self


class Form(BaseForm):
    """Form component."""

    form_fields: _t.List[FormField]
    """List of form fields."""

    type: _t.Literal['Form'] = 'Form'
    """The type of the component. Always 'Form'."""


FormFieldsModel = _t.TypeVar('FormFieldsModel', bound=pydantic.BaseModel)


class ModelForm(BaseForm):
    """Form component generated from a Pydantic model."""

    model: _t.Type[pydantic.BaseModel] = pydantic.Field(exclude=True)
    """Pydantic model from which to generate the form."""

    type: _t.Literal['ModelForm'] = 'ModelForm'
    """The type of the component. Always 'ModelForm'."""

    @pydantic.computed_field(alias='formFields')
    def form_fields(self) -> _t.List[FormField]:
        from ..json_schema import model_json_schema_to_fields

        return model_json_schema_to_fields(self.model)
