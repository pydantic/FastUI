from __future__ import annotations as _annotations

from datetime import date

from fastapi import FastAPI
from pydantic import RootModel, BaseModel, Field

import components as c
from components import AnyComponent
from components.events import PageEvent, GoToEvent

app = FastAPI()


class FastUi(RootModel):
    root: AnyComponent


@app.get('/api/', response_model=FastUi, response_model_exclude_none=True)
def read_root() -> AnyComponent:
    return c.Page(
        children=[
            c.Heading(text='Hello World'),
            c.Row(children=[
                c.Col(children=[c.Text(text='Hello World')]),
                c.Col(children=[c.Button(text='Show Modal', on_click=PageEvent(name='modal'))]),
                c.Col(children=[c.Button(text='View Table', on_click=GoToEvent(url='/table'))]),
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


class TableRow(BaseModel):
    name: str = Field(title='Name')
    dob: date = Field(title='Date of Birth')


@app.get('/api/table', response_model=FastUi, response_model_exclude_none=True)
def read_foo() -> AnyComponent:
    return c.Page(
        children=[
            c.Heading(text='Table'),
            c.Table[TableRow](
                rows=[
                    TableRow(name='John', dob=date(1990, 1, 1)),
                    TableRow(name='Jane', dob=date(1991, 1, 1)),
                ]
            )
        ]
    )
