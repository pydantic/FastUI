import typing as _t
from abc import ABC

import pydantic

from .. import class_name as _class_name

if _t.TYPE_CHECKING:
    pass


DataPoint = _t.TypeVar('DataPoint', bound=pydantic.BaseModel)


class BaseChart(pydantic.BaseModel, ABC, defer_build=True):
    title: str
    width: _t.Union[int, str] = '100%'
    height: _t.Union[int, str]
    data: _t.List[DataPoint]  # type: ignore
    class_name: _class_name.ClassNameField = None


class RechartsLineChart(BaseChart):
    type: _t.Literal['RechartsLineChart'] = 'RechartsLineChart'
    xKey: str
    yKeys: _t.List[str]
    yKeysNames: _t.Union[_t.List[str], None] = None
    colors: _t.List[str]
    tooltip: bool = True

    @pydantic.model_validator(mode='after')
    def check_length_of_y_keys_colors_and_y_keys_names(self):
        if len(self.yKeys) != len(self.colors):
            raise pydantic.ValidationError('Length of yKeys and colors must be the same')
        if self.yKeysNames and len(self.yKeys) != len(self.yKeysNames):
            raise pydantic.ValidationError('Length of yKeys and yKeysNames must be the same')
        return self
