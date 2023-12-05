from __future__ import annotations as _annotations

import json
import typing

import pandas as pd
import pydantic
from pandas.io.json import dumps as pdumps

if typing.TYPE_CHECKING:
    pass

InputHtmlType = typing.Literal['text', 'date', 'datetime-local', 'time', 'email', 'url', 'number', 'password']

import json
from typing import Dict, List, Literal, Optional, Union

import pandas as pd
from pandas.io.json import dumps as pdumps

EMPTY_DF_OBJ = {
    'schema': {'fields': [{'name': 'index', 'type': 'string'}], 'primaryKey': ['index'], 'pandas_version': '1.4.0'},
    'data': [],
}


def dumb_table_sumarize(df):
    """used when table_hints aren't provided.  Trests every column as a string"""
    table_hints = {col: {'is_numeric': False, 'type': 'obj', 'histogram': []} for col in df}
    table_hints['index'] = {'is_numeric': False, 'type': 'obj', 'histogram': []}
    return table_hints


def df_to_obj(df, order=None, table_hints=None):
    if order is None:
        order = df.columns
    obj = json.loads(df.to_json(orient='table', indent=2, default_handler=str))

    if isinstance(df.index, pd.MultiIndex):
        old_index = df.index
        temp_index = pd.Index(df.index.to_list(), tupleize_cols=False)
        df.index = temp_index
        obj = json.loads(df.to_json(orient='table', indent=2, default_handler=str))
        df.index = old_index
    else:
        obj = json.loads(df.to_json(orient='table', indent=2, default_handler=str))

    if table_hints is None:
        obj['table_hints'] = json.loads(pdumps(dumb_table_sumarize(df)))
    else:
        obj['table_hints'] = json.loads(pdumps(table_hints))

    index_name = df.index.name or 'index'
    fields = [{'name': index_name, 'type': 'unused'}]
    for c in order:
        fields.append({'name': str(c), 'type': 'unused'})
    obj['schema'] = dict(fields=fields, primaryKey=[index_name], pandas_version='1.4.0')
    return obj


# class BaseFormField(pydantic.BaseModel, ABC, defer_build=True):
#     name: str
#     title: str | list[str]
#     required: bool = False
#     error: str | None = None
#     locked: bool = False
#     description: str | None = None
#     class_name: _class_name.ClassName = None


class HistogramModel(pydantic.BaseModel):
    name: str
    population: float


HT = Optional[List[HistogramModel]]


# export interface ColumnStringHint {
#   type: 'string';
#   histogram?: any[];
# }


class ColumnStringHint(pydantic.BaseModel):
    type: Literal['string']
    histogram: HT


class ColumnObjHint(pydantic.BaseModel):
    type: Literal['obj']
    histogram: HT


# export interface ColumnBooleanHint {
#   type: 'boolean';
#   histogram?: any[];
# }


class ColumnBooleanHint(pydantic.BaseModel):
    type: Literal['boolean']
    histogram: HT


# export interface ColumnIntegertHint {
#   type: 'integer';
#   min_digits: number;
#   max_digits: number;
#   histogram: any[];
# }


class ColumnIntegerHint(pydantic.BaseModel):
    type: Literal['integer']
    min_digits: int
    max_digits: int
    histogram: HT


class DFColumn(pydantic.BaseModel):
    name: str
    type: str  # should be a union


ColumnHint = Union[ColumnStringHint, ColumnObjHint, ColumnBooleanHint, ColumnIntegerHint]


class DFSchema(pydantic.BaseModel):
    fields: list[DFColumn]
    primaryKey: list[str]  # ; //['index']
    pandas_version: str  # ; //'1.4.0',


# export type DFDataRow = Record<
#   string,
#   string | number | boolean | any[] | Record<string, any> | null
# >;

# export type DFData = DFDataRow[];

DFData = List[Dict[str, Union[str, int, float, None]]]


class DFWhole(pydantic.BaseModel):
    schema__: DFSchema = pydantic.Field(alias='schema')
    table_hints: dict[str, ColumnHint]
    data: DFData
    # data


class DFViewer(pydantic.BaseModel):
    type: Literal['DFViewer'] = 'DFViewer'
    df: DFWhole

    # Ilike the serialization_alias... but luckily I avoid the need because I don't have any snake cased fields
    # form_fields: list[FormField] = pydantic.Field(serialization_alias='formFields')
