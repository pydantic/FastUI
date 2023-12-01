from __future__ import annotations as _annotations

from collections import defaultdict
from enum import StrEnum
from typing import Annotated, Literal

from fastapi import APIRouter, Request, UploadFile
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.events import GoToEvent, PageEvent
from fastui.forms import FormFile, FormResponse, SelectSearchResponse, fastui_form
from httpx import AsyncClient
from pydantic import BaseModel, Field, SecretStr, field_validator
from pydantic_core import PydanticCustomError

from .shared import demo_page

router = APIRouter()


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
    search: str = Field(json_schema_extra={'search_url': '/api/forms/search'})
    searches: list[str] = Field(json_schema_extra={'search_url': '/api/forms/search'})

    @field_validator('name')
    def name_validator(cls, v: str) -> str:
        if v[0].islower():
            raise PydanticCustomError('lower', 'Name must start with a capital letter')
        return v


@router.get('/search', response_model=SelectSearchResponse)
async def search_view(request: Request, q: str) -> SelectSearchResponse:
    path_ends = f'name/{q}' if q else 'all'
    client: AsyncClient = request.app.state.httpx_client
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


@router.get('/{kind}', response_model=FastUI, response_model_exclude_none=True)
def form_view(kind: Literal['one', 'two', 'three']) -> list[AnyComponent]:
    return demo_page(
        c.LinkList(
            links=[
                c.Link(
                    components=[c.Text(text='Form One')],
                    on_click=PageEvent(name='change-form', push_path='/forms/one', context={'kind': 'one'}),
                    active='/forms/one',
                ),
                c.Link(
                    components=[c.Text(text='Form Two')],
                    on_click=PageEvent(name='change-form', push_path='/forms/two', context={'kind': 'two'}),
                    active='/forms/two',
                ),
                c.Link(
                    components=[c.Text(text='Form Three')],
                    on_click=PageEvent(name='change-form', push_path='/forms/three', context={'kind': 'three'}),
                    active='/forms/three',
                ),
            ],
            mode='tabs',
        ),
        c.ServerLoad(
            path='/forms/content/{kind}',
            load_trigger=PageEvent(name='change-form'),
            components=form_content(kind),
        ),
        title='Forms',
    )


@router.get('/content/{kind}', response_model=FastUI, response_model_exclude_none=True)
def form_content(kind: Literal['one', 'two', 'three']):
    match kind:
        case 'one':
            return [
                c.Heading(text='Form One', level=2),
                c.ModelForm[MyFormModel](
                    submit_url='/api/form',
                    success_event=PageEvent(name='form_success'),
                    # footer=[
                    #     c.Button(text='Cancel', on_click=GoToEvent(url='/')),
                    #     c.Button(text='Submit', html_type='submit'),
                    # ]
                ),
            ]
        case 'two':
            return [
                c.Heading(text='Form Two', level=2),
                c.ModelForm[MyFormModel](
                    submit_url='/api/form',
                    success_event=PageEvent(name='form_success'),
                ),
            ]
        case 'three':
            return [
                c.Heading(text='Form Three', level=2),
                c.ModelForm[MyFormModel](
                    submit_url='/api/form',
                    success_event=PageEvent(name='form_success'),
                ),
            ]
        case _:
            raise ValueError(f'Invalid kind {kind!r}')


@router.post('/form')
async def form_post(form: Annotated[MyFormModel, fastui_form(MyFormModel)]) -> FormResponse:
    return FormResponse(event=GoToEvent(url='/'))
