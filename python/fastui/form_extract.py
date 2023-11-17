import json
import typing

import fastapi
import pydantic
from starlette import datastructures

# from fastapi import Depends, HTTPException, Request
# from pydantic import BaseModel, ValidationError
# from starlette.datastructures import FormData
from . import events, json_schema

__all__ = 'FastUIForm', 'fastui_form', 'FormResponse'

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
            raise fastapi.HTTPException(status_code=422, detail={'form': e.errors()})

    return fastapi.Depends(run_fastui_form)


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
