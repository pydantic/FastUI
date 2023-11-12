from __future__ import annotations as _annotations

from datetime import date

from fastapi import FastAPI
from pydantic import BaseModel, Field

from fastui import components as c
from fastui import FastUI

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
def read_foo() -> AnyComponent:
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
                    c.Column(field='name', on_click=GoToEvent(url='/api/more/{id}/')),
                    c.Column(field='dob', display=c.Display.date),
                    c.Column(field='enabled'),
                ]
            )
        ]
    )
