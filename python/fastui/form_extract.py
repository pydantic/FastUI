import json
from typing import Any, Awaitable, Callable, Generic, TypeAlias, TypeVar

from fastapi import Depends, HTTPException, Request
from pydantic import BaseModel, ValidationError
from starlette.datastructures import FormData

from .json_schema import SchemeLocation

__all__ = 'FastUIForm', 'fastui_form'

FormModel = TypeVar('FormModel', bound=BaseModel)


class FastUIForm(Generic[FormModel]):
    """
    TODO mypy, pyright and pycharm don't understand the model type if this is used, is there a way to get it to work?
    """

    def __class_getitem__(cls, model: type[FormModel]) -> Callable[[Request], Awaitable[FormModel]]:
        return fastui_form(model)


def fastui_form(model: type[FormModel]) -> Callable[[Request], Awaitable[FormModel]]:
    async def run_fastui_form(request: Request):
        async with request.form() as form_data:
            model_data = unflatten(form_data)

        try:
            return model.model_validate(model_data)
        except ValidationError as e:
            raise HTTPException(status_code=422, detail={'form': e.errors()})

    return Depends(run_fastui_form)


NestedDict: TypeAlias = 'dict[str | int, NestedDict | str]'


def unflatten(form_data: FormData) -> NestedDict:
    """
    Unflatten a form data dict into a nested dict.
    """
    result_dict: NestedDict = {}
    for key, value in form_data.items():
        d: dict[str | int, Any] = result_dict

        *path, last_key = name_to_loc(key)
        for part in path:
            if part not in d:
                d[part] = {}
            d = d[part]

        d[last_key] = value
    return result_dict


def name_to_loc(name: str) -> SchemeLocation:
    if name.startswith('['):
        return json.loads(name)
    else:
        loc: SchemeLocation = []
        for part in name.split('.'):
            if part.isdigit():
                loc.append(int(part))
            else:
                loc.append(part)
        return loc
