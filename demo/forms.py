from __future__ import annotations as _annotations

import enum
from collections import defaultdict
from datetime import date
from typing import Annotated, Literal, TypeAlias

from fastapi import APIRouter, Request, UploadFile
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.events import GoToEvent, PageEvent
from fastui.forms import FormFile, SelectSearchResponse, fastui_form
from httpx import AsyncClient
from pydantic import BaseModel, EmailStr, Field, SecretStr, field_validator
from pydantic_core import PydanticCustomError

from .shared import demo_page

router = APIRouter()


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


FormKind: TypeAlias = Literal['login', 'select', 'big']


@router.get('/{kind}', response_model=FastUI, response_model_exclude_none=True)
def forms_view(kind: FormKind) -> list[AnyComponent]:
    return demo_page(
        c.LinkList(
            links=[
                c.Link(
                    components=[c.Text(text='Login Form')],
                    on_click=PageEvent(name='change-form', push_path='/forms/login', context={'kind': 'login'}),
                    active='/forms/login',
                ),
                c.Link(
                    components=[c.Text(text='Select Form')],
                    on_click=PageEvent(name='change-form', push_path='/forms/select', context={'kind': 'select'}),
                    active='/forms/select',
                ),
                c.Link(
                    components=[c.Text(text='Big Form')],
                    on_click=PageEvent(name='change-form', push_path='/forms/big', context={'kind': 'big'}),
                    active='/forms/big',
                ),
            ],
            mode='tabs',
            class_name='+ mb-4',
        ),
        c.ServerLoad(
            path='/forms/content/{kind}',
            load_trigger=PageEvent(name='change-form'),
            components=form_content(kind),
        ),
        title='Forms',
    )


@router.get('/content/{kind}', response_model=FastUI, response_model_exclude_none=True)
def form_content(kind: FormKind):
    match kind:
        case 'login':
            return [
                c.Heading(text='Login Form', level=2),
                c.Paragraph(text='Simple login form with email and password.'),
                c.ModelForm(model=LoginForm, submit_url='/api/forms/login'),
            ]
        case 'select':
            return [
                c.Heading(text='Select Form', level=2),
                c.Paragraph(text='Form showing different ways of doing select.'),
                c.ModelForm(model=SelectForm, submit_url='/api/forms/select'),
            ]
        case 'big':
            return [
                c.Heading(text='Large Form', level=2),
                c.Paragraph(text='Form with a lot of fields.'),
                c.ModelForm(model=BigModel, submit_url='/api/forms/big'),
            ]
        case _:
            raise ValueError(f'Invalid kind {kind!r}')


class LoginForm(BaseModel):
    email: EmailStr = Field(title='Email Address', description="Try 'x@y' to trigger server side validation")
    password: SecretStr


@router.post('/login', response_model=FastUI, response_model_exclude_none=True)
async def login_form_post(form: Annotated[LoginForm, fastui_form(LoginForm)]):
    print(form)
    return [c.FireEvent(event=GoToEvent(url='/'))]


class ToolEnum(str, enum.Enum):
    hammer = 'hammer'
    screwdriver = 'screwdriver'
    saw = 'saw'
    claw_hammer = 'claw_hammer'


class SelectForm(BaseModel):
    select_single: ToolEnum = Field(title='Select Single')
    select_multiple: list[ToolEnum] = Field(title='Select Multiple')
    search_select_single: str = Field(json_schema_extra={'search_url': '/api/forms/search'})
    search_select_multiple: list[str] = Field(json_schema_extra={'search_url': '/api/forms/search'})


@router.post('/select', response_model=FastUI, response_model_exclude_none=True)
async def select_form_post(form: Annotated[SelectForm, fastui_form(SelectForm)]):
    # print(form)
    return [c.FireEvent(event=GoToEvent(url='/'))]


class SizeModel(BaseModel):
    width: int = Field(description='This is a field of a nested model')
    height: int = Field(description='This is a field of a nested model')


class BigModel(BaseModel):
    name: str | None = Field(
        None, description='This field is not required, it must start with a capital letter if provided'
    )
    profile_pic: Annotated[UploadFile, FormFile(accept='image/*', max_size=16_000)] = Field(
        description='Upload a profile picture, must not be more than 16kb'
    )
    profile_pics: Annotated[list[UploadFile], FormFile(accept='image/*')] | None = Field(
        None, description='Upload multiple images'
    )
    dob: date = Field(title='Date of Birth', description='Your date of birth, this is required hence bold')
    human: bool | None = Field(
        None, title='Is human', description='Are you human?', json_schema_extra={'mode': 'switch'}
    )
    size: SizeModel

    position: tuple[
        Annotated[int, Field(description='X Coordinate')],
        Annotated[int, Field(description='Y Coordinate')],
    ]

    @field_validator('name')
    def name_validator(cls, v: str | None) -> str:
        if v and v[0].islower():
            raise PydanticCustomError('lower', 'Name must start with a capital letter')
        return v


@router.post('/big', response_model=FastUI, response_model_exclude_none=True)
async def big_form_post(form: Annotated[BigModel, fastui_form(BigModel)]):
    print(form)
    return [c.FireEvent(event=GoToEvent(url='/'))]
