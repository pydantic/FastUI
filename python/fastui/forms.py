from __future__ import annotations as _annotations

import json
import typing
from itertools import groupby
from operator import itemgetter

import pydantic
import pydantic_core
import typing_extensions
from pydantic_core import core_schema

from . import events

try:
    import fastapi
    from starlette import datastructures as ds
except ImportError as e:
    raise ImportError('fastui.dev requires fastapi to be installed, install with `pip install fastui[fastapi]`') from e

if typing.TYPE_CHECKING:
    from . import json_schema

__all__ = 'FastUIForm', 'fastui_form', 'FormResponse', 'FormFile', 'SelectSearchResponse', 'SelectOption'

FormModel = typing.TypeVar('FormModel', bound=pydantic.BaseModel)


class FastUIForm(typing.Generic[FormModel]):
    """
    TODO mypy, pyright and pycharm don't understand the model type if this is used, is there a way to get it to work?
    """

    def __class_getitem__(
        cls, model: type[FormModel]
    ) -> typing.Callable[[fastapi.Request], typing.Awaitable[FormModel]]:
        return fastui_form(model)


def fastui_form(model: type[FormModel]) -> typing.Callable[[fastapi.Request], typing.Awaitable[FormModel]]:
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

    def __init__(self, accept: str | None = None, max_size: int | None = None):
        self.accept = accept
        self.max_size = max_size

    def validate_single(self, input_value: typing.Any) -> ds.UploadFile:
        if isinstance(input_value, ds.UploadFile):
            file = input_value
            self._validate_file(file)
            return file
        else:
            raise pydantic_core.PydanticCustomError('not_file', 'Input is not a file')

    def validate_multiple(self, input_value: typing.Any) -> list[ds.UploadFile]:
        if isinstance(input_value, list):
            return [self.validate_single(v) for v in input_value]
        else:
            return [self.validate_single(input_value)]

    def _validate_file(self, file: ds.UploadFile) -> None:
        """
        See https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file#unique_file_type_specifiers
        for details on what's allowed
        """
        if file.size == 0:
            # FIXME is this right???
            return

        if self.max_size is not None and file.size is not None and file.size > self.max_size:
            raise pydantic_core.PydanticCustomError(
                'file_no_big',
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
            elif file.content_type is None:
                continue
            elif accept.endswith('/*'):
                if file.content_type.startswith(accept[:-1]):
                    return
            elif file.content_type == accept:
                return

        raise pydantic_core.PydanticCustomError(
            'accept_mismatch',
            (
                'Uploaded file "{filename}" with content type "{content_type}" '
                'does not match accept criteria "{accept}"'
            ),
            {'filename': file.filename, 'content_type': file.content_type, 'accept': self.accept},
        )

    def __get_pydantic_core_schema__(self, source_type: type[typing.Any], *_args) -> core_schema.CoreSchema:
        if issubclass(source_type, ds.UploadFile):
            return core_schema.no_info_plain_validator_function(self.validate_single)
        elif typing.get_origin(source_type) == list:
            args = typing.get_args(source_type)
            if len(args) == 1 and issubclass(args[0], ds.UploadFile):
                return core_schema.no_info_plain_validator_function(self.validate_multiple)

        raise TypeError(f'FormFile can only be used with `UploadFile` or `list[UploadFile]`, not {source_type}')

    def __get_pydantic_json_schema__(self, core_schema_: core_schema.CoreSchema, *_args) -> json_schema.JsonSchemaAny:
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


class FormResponse(pydantic.BaseModel):
    event: events.AnyEvent
    type: typing.Literal['FormResponse'] = 'FormResponse'


class SelectOption(typing_extensions.TypedDict):
    value: str
    label: str


class SelectGroup(typing_extensions.TypedDict):
    label: str
    options: list[SelectOption]


class SelectSearchResponse(pydantic.BaseModel):
    options: list[SelectOption] | list[SelectGroup]


NestedDict: typing.TypeAlias = 'dict[str | int, NestedDict | str | list[str] | ds.UploadFile | list[ds.UploadFile]]'


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

        d: dict[str | int, typing.Any] = result_dict

        *path, last_key = name_to_loc(key)
        for part in path:
            if part not in d:
                d[part] = {}
            d = d[part]

        if len(values) == 1:
            d[last_key] = values[0]
        else:
            d[last_key] = values

    return result_dict


def name_to_loc(name: str) -> json_schema.SchemeLocation:
    if name.startswith('['):
        return json.loads(name)
    else:
        loc: json_schema.SchemeLocation = []
        for part in name.split('.'):
            if part.isdigit():
                loc.append(int(part))
            else:
                loc.append(part)
        return loc
