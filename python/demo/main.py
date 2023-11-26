from __future__ import annotations as _annotations

import asyncio
from collections import defaultdict
from datetime import date
from enum import StrEnum
from typing import Annotated, Literal

from fastapi import UploadFile
from fastui import AnyComponent, FastUI, dev_fastapi_app
from fastui import components as c
from fastui.display import Display
from fastui.events import GoToEvent, PageEvent
from fastui.forms import FormFile, FormResponse, SelectSearchResponse, fastui_form
from httpx import AsyncClient
from pydantic import BaseModel, Field, SecretStr, field_validator
from pydantic_core import PydanticCustomError

# app = FastAPI()
app = dev_fastapi_app()


def navbar() -> AnyComponent:
    return c.Navbar(
        title='FastUI Demo',
        links=[
            c.Link(components=[c.Text(text='Home')], on_click=GoToEvent(url='/'), active='/'),
            c.Link(components=[c.Text(text='Table')], on_click=GoToEvent(url='/table'), active='/table'),
            c.Link(components=[c.Text(text='Forms')], on_click=GoToEvent(url='/form/one'), active='startswith:/form'),
        ],
    )


def panel(*components: AnyComponent) -> AnyComponent:
    return c.Div(class_name='col border rounded m-1 p-2 pb-3', components=list(components))


@app.get('/api/', response_model=FastUI, response_model_exclude_none=True)
def read_root() -> list[AnyComponent]:
    return [
        c.PageTitle(text='FastUI Demo'),
        navbar(),
        c.Page(
            components=[
                c.Heading(text='Modal and Flex examples'),
                c.Paragraph(text='Below is an example of a flex container with 3 panels.'),
                c.Markdown(
                    text="""\
This is some **Markdown**, link to [table](/table).

```python
x = 1
y = 2
assert x + y == 3
```

"""
                ),
                c.Div(
                    class_name='row',
                    components=[
                        panel(
                            c.Heading(text='Panel 1', level=3),
                            c.Paragraph(text='This is a div with a border and rounded corners.'),
                        ),
                        panel(
                            c.Heading(text='Panel 2', level=3),
                            c.Paragraph(text='Click the link below to open a modal with content included directly'),
                            c.Button(text='Show Static Modal', on_click=PageEvent(name='static-modal')),
                        ),
                        panel(
                            c.Heading(text='Panel 3', level=3),
                            c.Paragraph(
                                text=(
                                    'Click the link below to open a modal with content loaded from the '
                                    'server when the modal is opened.'
                                )
                            ),
                            c.Button(text='Show Dynamic Modal', on_click=PageEvent(name='dynamic-modal')),
                        ),
                    ],
                ),
                c.Modal(
                    title='Static Modal',
                    body=[c.Paragraph(text='This is some static content in a modal.')],
                    footer=[
                        c.Button(text='Close', on_click=PageEvent(name='static-modal')),
                    ],
                    open_trigger=PageEvent(name='static-modal'),
                ),
                c.Modal(
                    title='Dynamic Modal',
                    body=[c.ServerLoad(url='/modal')],
                    footer=[
                        c.Button(text='Close', on_click=PageEvent(name='dynamic-modal')),
                    ],
                    open_trigger=PageEvent(name='dynamic-modal'),
                ),
            ],
        ),
    ]


class MyTableRow(BaseModel):
    id: int = Field(title='ID')
    name: str = Field(title='Name')
    dob: date = Field(title='Date of Birth')
    enabled: bool | None = None


@app.get('/api/modal', response_model=FastUI, response_model_exclude_none=True)
async def modal_view() -> list[AnyComponent]:
    await asyncio.sleep(0.5)
    return [c.Text(text='Modal Content Dynamic')]


@app.get('/api/table', response_model=FastUI, response_model_exclude_none=True)
def table_view() -> list[AnyComponent]:
    return [
        navbar(),
        c.PageTitle(text='FastUI Demo - Table'),
        c.Page(
            components=[
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
        ),
    ]


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
    name: str = Field(default='foobar', title='Name', min_length=3, description='Your name')
    # tool: ToolEnum = Field(json_schema_extra={'enum_labels': {'hammer': 'Big Hammer'}})
    task: Literal['build', 'destroy'] | None = 'build'
    tasks: set[Literal['build', 'destroy']]
    profile_pic: Annotated[UploadFile, FormFile(accept='image/*', max_size=16_000)]
    # profile_pics: Annotated[list[UploadFile], FormFile(accept='image/*', max_size=400)]
    # binary: bytes

    # dob: date = Field(title='Date of Birth', description='Your date of birth')
    # weight: typing.Annotated[int, annotated_types.Gt(0)]
    # size: PositiveInt = None
    # enabled: bool = False
    # nested: NestedFormModel
    password: SecretStr
    search: str = Field(json_schema_extra={'search_url': '/api/search'})
    searches: list[str] = Field(json_schema_extra={'search_url': '/api/search'})

    @field_validator('name')
    def name_validator(cls, v: str) -> str:
        if v[0].islower():
            raise PydanticCustomError('lower', 'Name must start with a capital letter')
        return v


@app.get('/api/search', response_model=SelectSearchResponse)
async def search_view(q: str) -> SelectSearchResponse:
    async with AsyncClient() as client:
        path_ends = f'name/{q}' if q else 'all'
        r = await client.get(f'https://restcountries.com/v3.1/{path_ends}')
        if r.status_code == 404:
            options = []
        else:
            r.raise_for_status()
            data = r.json()
            if path_ends == 'all':
                # if we got all, filter to the 20 most populous countries
                data.sort(key=lambda x: x['population'], reverse=True)
                data = data[0:20]
                data.sort(key=lambda x: x['name']['common'])

            regions = defaultdict(list)
            for co in data:
                regions[co['region']].append({'value': co['cca3'], 'label': co['name']['common']})
            options = [{'label': k, 'options': v} for k, v in regions.items()]
    return SelectSearchResponse(options=options)


@app.get('/api/form/{kind}', response_model=FastUI, response_model_exclude_none=True)
def form_view(kind: str) -> list[AnyComponent]:
    return [
        navbar(),
        c.PageTitle(text='FastUI Demo - Form Examples'),
        c.Page(
            components=[
                c.Heading(text='Form'),
                c.LinkList(
                    links=[
                        c.Link(
                            components=[c.Text(text='Form One')],
                            on_click=GoToEvent(url='/form/one'),
                            active='/form/one',
                        ),
                        c.Link(
                            components=[c.Text(text='Form Two')],
                            on_click=GoToEvent(url='/form/two'),
                            active='/form/two',
                        ),
                        c.Link(
                            components=[c.Text(text='Form Three')],
                            on_click=GoToEvent(url='/form/three'),
                            active='/form/three',
                        ),
                    ],
                    mode='tabs',
                ),
                c.ModelForm[MyFormModel](
                    submit_url='/api/form',
                    success_event=PageEvent(name='form_success'),
                    # footer=[
                    #     c.Button(text='Cancel', on_click=GoToEvent(url='/')),
                    #     c.Button(text='Submit', html_type='submit'),
                    # ]
                ),
            ]
        ),
    ]


@app.post('/api/form')
async def form_post(form: Annotated[MyFormModel, fastui_form(MyFormModel)]) -> FormResponse:
    debug(form)
    return FormResponse(event=GoToEvent(url='/'))
