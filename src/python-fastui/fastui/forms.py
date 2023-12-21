import json
import typing as _t
from itertools import groupby
from mimetypes import MimeTypes
from operator import itemgetter

import pydantic
import pydantic_core
import typing_extensions as _te
from pydantic_core import core_schema

try:
    import fastapi
    from fastapi import params as fastapi_params
    from starlette import datastructures as ds
except ImportError as _e:
    raise ImportError('fastui.dev requires fastapi to be installed, install with `pip install fastui[fastapi]`') from _e

if _t.TYPE_CHECKING:
    from . import json_schema

__all__ = 'FastUIForm', 'fastui_form', 'FormFile', 'SelectSearchResponse', 'SelectOption'

FormModel = _t.TypeVar('FormModel', bound=pydantic.BaseModel)


class FastUIForm(_t.Generic[FormModel]):
    """
    TODO mypy, pyright and pycharm don't understand the model type if this is used, is there a way to get it to work?
    """

    def __class_getitem__(cls, model: _t.Type[FormModel]) -> fastapi_params.Depends:
        return fastui_form(model)


def fastui_form(model: _t.Type[FormModel]) -> fastapi_params.Depends:
    async def run_fastui_form(request: fastapi.Request):
        async with request.form() as form_data:
            model_data = unflatten(form_data)

        try:
            return model.model_validate(model_data)
        except pydantic.ValidationError as e:
            raise fastapi.HTTPException(
                status_code=422,
                detail={'form': e.errors(include_input=False, include_url=False, include_context=False)},
            )

    return fastapi.Depends(run_fastui_form)


class FormFile:
    __slots__ = 'accept', 'max_size'

    def __init__(self, accept: _t.Union[str, None] = None, max_size: _t.Union[int, None] = None):
        self.accept = accept
        self.max_size = max_size

    def validate_single(self, input_value: _t.Any) -> ds.UploadFile:
        if isinstance(input_value, ds.UploadFile):
            file = input_value
            self._validate_file(file)
            return file
        else:
            raise pydantic_core.PydanticCustomError('not_file', 'Input is not a file')

    def validate_multiple(self, input_value: _t.Any) -> _t.List[ds.UploadFile]:
        if isinstance(input_value, list):
            return [self.validate_single(v) for v in input_value]
        else:
            return [self.validate_single(input_value)]

    def _validate_file(self, file: ds.UploadFile) -> None:
        """
        See https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file#unique_file_type_specifiers
        for details on what's allowed.
        """
        if file.size == 0:
            # FIXME is this right???
            return

        if self.max_size is not None and file.size is not None and file.size > self.max_size:
            raise pydantic_core.PydanticCustomError(
                'file_too_big',
                'File size was {file_size}, exceeding maximum allowed size of {max_size}',
                {
                    'file_size': pydantic.ByteSize(file.size).human_readable(),
                    'max_size': pydantic.ByteSize(self.max_size).human_readable(),
                },
            )

        if self.accept is None:
            return

        for accept in self.accept.split(','):
            accept = accept.strip()
            if accept == '*/*':
                return
            elif accept.startswith('.'):
                # this is a file extension
                if file.filename and file.filename.endswith(accept):
                    return

            if content_type := get_content_type(file):
                if accept.endswith('/*'):
                    if content_type.startswith(accept[:-1]):
                        return
                elif content_type == accept:
                    return

        raise pydantic_core.PydanticCustomError(
            'accept_mismatch',
            (
                'Uploaded file "{filename}" with content type "{content_type}" '
                'does not match accept criteria "{accept}"'
            ),
            {'filename': file.filename, 'content_type': file.content_type, 'accept': self.accept},
        )

    def __get_pydantic_core_schema__(self, source_type: _t.Type[_t.Any], *_args) -> core_schema.CoreSchema:
        if _t.get_origin(source_type) == list:
            args = _t.get_args(source_type)
            if len(args) == 1 and issubclass(args[0], ds.UploadFile):
                return core_schema.no_info_plain_validator_function(self.validate_multiple)
        elif issubclass(source_type, ds.UploadFile):
            return core_schema.no_info_plain_validator_function(self.validate_single)

        raise TypeError(f'FormFile can only be used with `UploadFile` or `list[UploadFile]`, not {source_type}')

    def __get_pydantic_json_schema__(self, core_schema_: core_schema.CoreSchema, *_args) -> 'json_schema.JsonSchemaAny':
        from . import json_schema

        s = json_schema.JsonSchemaFile(type='string', format='binary')
        if self.accept:
            s['accept'] = self.accept

        function = core_schema_.get('function', {}).get('function')
        if function and function.__name__ == 'validate_multiple':
            s = json_schema.JsonSchemaArray(type='array', items=s)
        return s

    def __repr__(self):
        return f'FormFile(accept={self.accept!r})'


_mime_types = MimeTypes()


def get_content_type(file: ds.UploadFile) -> _t.Union[str, None]:
    if file.content_type:
        return file.content_type
    elif file.filename:
        return _mime_types.guess_type(file.filename)[0]


class SelectOption(_te.TypedDict):
    value: str
    label: str


class SelectGroup(_te.TypedDict):
    label: str
    options: _t.List[SelectOption]


SelectOptions = _te.TypeAliasType('SelectOptions', _t.Union[_t.List[SelectOption], _t.List[SelectGroup]])


class SelectSearchResponse(pydantic.BaseModel):
    options: SelectOptions


NestedDict: _te.TypeAlias = 'dict[str | int, NestedDict | str | list[str] | ds.UploadFile | list[ds.UploadFile]]'


def unflatten(form_data: ds.FormData) -> NestedDict:
    """
    Unflatten a `FormData` dict into a nested dict.

    Also omit empty strings, this might be a bit controversial, but it helps in many scenarios, e.g. a select
    which hasn't been updated. It also avoids empty values for string inputs that haven't been fill in.
    """
    result_dict: NestedDict = {}
    for key, g in groupby(form_data.multi_items(), itemgetter(0)):
        values = [v for _, v in g]
        if values == ['']:
            continue

        d: _t.Dict[_t.Union[str, int], _t.Any] = result_dict

        *path, last_key = name_to_loc(key)
        for part in path:
            if part not in d:
                d[part] = {}
            d = d[part]

        if len(values) == 1:
            d[last_key] = values[0]
        else:
            d[last_key] = values

    # this logic takes care of converting `dict[int, str]` to `list[str]`
    # we recursively process each dict in `result_dict` and convert it to a list if all keys are ints
    dicts = [result_dict]
    while dicts:
        d = dicts.pop()
        for key, value in d.items():
            if isinstance(value, dict):
                if all(isinstance(k, int) for k in value):
                    # sort key-value pairs based on the keys, then take just the values as a list
                    d[key] = [v for _, v in sorted(value.items())]
                else:
                    dicts.append(value)

    return result_dict


def name_to_loc(name: str) -> 'json_schema.SchemeLocation':
    if name.startswith('['):
        return json.loads(name)
    else:
        loc: 'json_schema.SchemeLocation' = []
        for part in name.split('.'):
            if part.isdigit():
                loc.append(int(part))
            else:
                loc.append(part)
        return loc
