from __future__ import annotations as _annotations

import json
import typing
from dataclasses import dataclass

import fastapi
import pydantic
import pydantic_core
from pydantic_core import core_schema
from starlette import datastructures

# from fastapi import Depends, HTTPException, Request
# from pydantic import BaseModel, ValidationError
# from starlette.datastructures import FormData
from . import events, json_schema

__all__ = 'FastUIForm', 'fastui_form', 'FormResponse', 'FormFile', 'FileAccept', 'FormValidationError'

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


def file_upload_validate(input_value: typing.Any) -> datastructures.UploadFile:
    if isinstance(input_value, datastructures.UploadFile):
        return input_value
    else:
        raise pydantic_core.PydanticCustomError('not_file', 'Input is not a file')


FormFile = typing.Annotated[
    datastructures.UploadFile,
    pydantic.PlainValidator(file_upload_validate),
    pydantic.WithJsonSchema(json_schema=json_schema.JsonSchemaFile(type='string', format='file')),  # type: ignore
]


@dataclass
class FileAccept:
    accept: str

    def validate(self, input_value: typing.Any) -> datastructures.UploadFile:
        """
        See https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file#unique_file_type_specifiers
        for details on what's allowed
        """
        file = file_upload_validate(input_value)
        for accept in self.accept.split(','):
            accept = accept.strip()
            if accept == '*/*':
                return file
            elif accept.startswith('.'):
                # this is a file extension
                if file.filename and file.filename.endswith(accept):
                    return file
            elif file.content_type is None:
                continue
            elif accept.endswith('/*'):
                if file.content_type.startswith(accept[:-1]):
                    return file
            elif file.content_type == accept:
                return file
        raise pydantic_core.PydanticCustomError(
            'accept_mismatch',
            (
                'Uploaded file "{filename}" with content type "{content_type}" '
                'does not match accept criteria "{accept}"'
            ),
            {'filename': file.filename, 'content_type': file.content_type, 'accept': self.accept},
        )

    def __get_pydantic_core_schema__(self, *_args) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(self.validate)

    def __get_pydantic_json_schema__(self, *_args) -> json_schema.JsonSchemaFile:
        # return json_schema.JsonSchemaFile(type='string', format='file', accept=self.accept)
        return json_schema.JsonSchemaFile(type='string', format='file')


class FormResponse(pydantic.BaseModel):
    event: events.Event
    type: typing.Literal['FormResponse'] = 'FormResponse'


NestedDict: typing.TypeAlias = 'dict[str | int, NestedDict | str]'


def unflatten(form_data: datastructures.FormData) -> NestedDict:
    """
    Unflatten a `FormData` dict into a nested dict.

    Also omit empty strings, this might be a bit controversial, but it helps in many scenarios, e.g. a select
    which hasn't been updated. It also avoids empty values for string inputs that haven't been fill in.
    """
    result_dict: NestedDict = {}
    for key, value in form_data.items():
        if value == '':
            continue

        d: dict[str | int, typing.Any] = result_dict

        *path, last_key = name_to_loc(key)
        for part in path:
            if part not in d:
                d[part] = {}
            d = d[part]

        d[last_key] = value
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
