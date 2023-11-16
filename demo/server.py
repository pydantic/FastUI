from __future__ import annotations as _annotations

import typing
from datetime import date

import annotated_types
from fastapi import FastAPI
from pydantic import BaseModel, Field, HttpUrl

from fastui import components as c
from fastui import FastUI, AnyComponent
from fastui.display import Display
from fastui.events import PageEvent, GoToEvent

app = FastAPI()


@app.get('/api/', response_model=FastUI, response_model_exclude_none=True)
def read_root() -> AnyComponent:
    return c.Page(
        children=[
            c.Heading(text='Hello World'),
            c.Row(children=[
                c.Col(children=[c.Text(text='Hello World')]),
                c.Col(children=[c.Button(text='Show Modal', on_click=PageEvent(name='modal'))]),
                c.Col(children=[c.Button(text='View Table', on_click=GoToEvent(url='/table'))]),
                c.Col(children=[c.Button(text='Form', on_click=GoToEvent(url='/form'))]),
            ]),
            c.Modal(
                title='Modal Title',
                body=[c.Text(text='Modal Content')],
                footer=[c.Button(text='Close', on_click=PageEvent(name='modal'))],
                open_trigger=PageEvent(name='modal'),
            ),
        ],
        class_name='+ mt-4'
    )


class MyTableRow(BaseModel):
    id: int = Field(title='ID')
    name: str = Field(title='Name')
    dob: date = Field(title='Date of Birth')
    enabled: bool | None = None


@app.get('/api/table', response_model=FastUI, response_model_exclude_none=True)
def table_view() -> AnyComponent:
    return c.Page(
        children=[
            c.Heading(text='Table'),
            c.Table[MyTableRow](
                data=[
                    MyTableRow(id=1, name='John', dob=date(1990, 1, 1), enabled=True),
                    MyTableRow(id=2, name='Jane', dob=date(1991, 1, 1), enabled=False),
                    MyTableRow(id=3, name='Jack', dob=date(1992, 1, 1)),
                ],
                columns=[
                    c.TableColumn(field='name', on_click=GoToEvent(url='/more/{id}/')),
                    c.TableColumn(field='dob', display=Display.date),
                    c.TableColumn(field='enabled'),
                ]
            )
        ]
    )


class NestedFormModel(BaseModel):
    # x: int
    # profile_view: HttpUrl
    profile_view: str


class MyFormModel(BaseModel):
    name: str = Field(default='foobar', title='Name')
    # dob: date = Field(title='Date of Birth', description='Your date of birth')
    # weight: typing.Annotated[int, annotated_types.Gt(0)]
    # size: float = None
    enabled: bool = None
    nested: NestedFormModel


@app.get('/api/form', response_model=FastUI, response_model_exclude_none=True)
def form_view() -> AnyComponent:
    f = c.Page(
        children=[
            c.Heading(text='Form'),
            c.ModelForm[MyFormModel](submit_url='/api/form', success_event=PageEvent(name='form_success'))
        ]
    )
    debug(f)
    return f


@app.post('/api/form')
def form_post():
    return {'success': True}
