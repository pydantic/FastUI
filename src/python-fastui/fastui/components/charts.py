import typing as _t
from abc import ABC

import pydantic as _p

from .. import class_name as _class_name

if _t.TYPE_CHECKING:
    pass


DataPoint = _t.TypeVar('DataPoint', bound=_p.BaseModel)


class BaseChart(_p.BaseModel, ABC, defer_build=True):
    title: str
    width: _t.Union[int, str] = '100%'
    height: _t.Union[int, str]
    data: _t.List[DataPoint]  # type: ignore
    class_name: _class_name.ClassNameField = None


class RechartsLineChart(BaseChart):
    type: _t.Literal['RechartsLineChart'] = 'RechartsLineChart'
    x_key: str = _p.Field(..., serialization_alias='xKey')
    y_keys: _t.List[str] = _p.Field(..., serialization_alias='yKeys')
    y_keys_names: _t.Union[_t.List[str], None] = _p.Field(None, serialization_alias='yKeysNames')
    colors: _t.List[str]
    tooltip: bool = True

    @_p.model_validator(mode='after')
    def check_length_of_y_keys_colors_and_y_keys_names(self):
        if len(self.y_keys) != len(self.colors):
            raise _p.ValidationError('Length of y_keys and colors must be the same')
        if self.y_keys_names and len(self.y_keys) != len(self.y_keys_names):
            raise _p.ValidationError('Length of y_keys and y_keys_names must be the same')
        return self
