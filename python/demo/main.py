from __future__ import annotations as _annotations

import asyncio
from datetime import date
from enum import StrEnum
from typing import Annotated, Literal

from fastapi import UploadFile
from fastui import AnyComponent, FastUI, dev_fastapi_app
from fastui import components as c
from fastui.display import Display
from fastui.events import GoToEvent, PageEvent
from fastui.forms import FormFile, FormResponse, fastui_form
from pydantic import BaseModel, Field

# app = FastAPI()
app = dev_fastapi_app()


@app.get('/api/', response_model=FastUI, response_model_exclude_none=True)
def read_root() -> AnyComponent:
    return c.Page(
        children=[
            c.Heading(text='Hello World'),
            c.Row(
                children=[
                    c.Col(children=[c.Text(text='Hello World')]),
                    c.Col(children=[c.Button(text='Show Modal', on_click=PageEvent(name='modal'))]),
                    c.Col(children=[c.Button(text='View Table', on_click=GoToEvent(url='/table'))]),
                    c.Col(children=[c.Button(text='Form', on_click=GoToEvent(url='/form'))]),
                ]
            ),
            c.Modal(
                title='Modal Title',
                body=[c.ServerLoad(url='/modal')],
                footer=[c.Button(text='Close', on_click=PageEvent(name='modal'))],
                open_trigger=PageEvent(name='modal'),
            ),
        ],
        class_name='+ mt-4',
    )


class MyTableRow(BaseModel):
    id: int = Field(title='ID')
    name: str = Field(title='Name')
    dob: date = Field(title='Date of Birth')
    enabled: bool | None = None


@app.get('/api/modal', response_model=FastUI, response_model_exclude_none=True)
async def modal_view() -> AnyComponent:
    await asyncio.sleep(2)
    return c.Text(text='Modal Content Dynamic')


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
                ],
            ),
        ]
    )


class NestedFormModel(BaseModel):
    # x: int
    # profile_view: HttpUrl
    profile_view: str


class ToolEnum(StrEnum):
    hammer = 'hammer'
    screwdriver = 'screwdriver'
    saw = 'saw'
    claw_hammer = 'claw_hammer'


class MyFormModel(BaseModel):
    name: str = Field(default='foobar', title='Name')
    # tool: ToolEnum = Field(json_schema_extra={'enum_display_values': {'hammer': 'Big Hammer'}})
    task: Literal['build', 'destroy'] | None = None
    profile_pic: Annotated[UploadFile, FormFile(accept='image/*', max_size=16_000)]
    # profile_pics: Annotated[list[UploadFile], FormFile(accept='image/*', max_size=400)]
    # binary: bytes

    # dob: date = Field(title='Date of Birth', description='Your date of birth')
    # weight: typing.Annotated[int, annotated_types.Gt(0)]
    # size: PositiveInt = None
    # enabled: bool = False
    # nested: NestedFormModel


@app.get('/api/form', response_model=FastUI, response_model_exclude_none=True)
def form_view() -> AnyComponent:
    return c.Page(
        children=[
            c.Heading(text='Form'),
            c.ModelForm[MyFormModel](
                submit_url='/api/form',
                success_event=PageEvent(name='form_success'),
                # footer=[
                #     c.Button(text='Cancel', on_click=GoToEvent(url='/')),
                #     c.Button(text='Submit', html_type='submit'),
                # ]
            ),
        ]
    )


@app.post('/api/form')
async def form_post(form: Annotated[MyFormModel, fastui_form(MyFormModel)]) -> FormResponse:
    debug(form)
    return FormResponse(event=GoToEvent(url='/'))
