from __future__ import annotations as _annotations

import os
from typing import Annotated, Literal, TypeAlias

from fastapi import APIRouter, Depends, Header, Request
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.auth import AuthError, GitHubAuthProvider
from fastui.events import AuthEvent, GoToEvent, PageEvent
from fastui.forms import fastui_form
from httpx import AsyncClient
from pydantic import BaseModel, EmailStr, Field, SecretStr

from . import db
from .shared import demo_page

router = APIRouter()


async def get_user(authorization: Annotated[str, Header()] = '') -> db.User | None:
    try:
        token = authorization.split(' ', 1)[1]
    except IndexError:
        return None
    else:
        return await db.get_user(token)


# this will give an error when making requests to GitHub, but at least the app will run
GITHUB_CLIENT_SECRET = SecretStr(os.getenv('GITHUB_CLIENT_SECRET', 'dummy-secret'))


async def get_github_auth(request: Request) -> GitHubAuthProvider:
    client: AsyncClient = request.app.state.httpx_client
    return GitHubAuthProvider(
        httpx_client=client,
        github_client_id='9eddf87b27f71f52194a',
        github_client_secret=GITHUB_CLIENT_SECRET,
    )


LoginKind: TypeAlias = Literal['password', 'github']


@router.get('/login/{kind}', response_model=FastUI, response_model_exclude_none=True)
async def auth_login(
    kind: LoginKind,
    user: Annotated[str | None, Depends(get_user)],
    github_auth: Annotated[GitHubAuthProvider, Depends(get_github_auth)],
) -> list[AnyComponent]:
    if user is None:
        return demo_page(
            c.LinkList(
                links=[
                    c.Link(
                        components=[c.Text(text='Password Login')],
                        on_click=PageEvent(name='tab', push_path='/auth/login/password', context={'kind': 'password'}),
                        active='/auth/login/password',
                    ),
                    c.Link(
                        components=[c.Text(text='GitHub Login')],
                        on_click=PageEvent(name='tab', push_path='/auth/login/github', context={'kind': 'github'}),
                        active='/auth/login/github',
                    ),
                ],
                mode='tabs',
                class_name='+ mb-4',
            ),
            c.ServerLoad(
                path='/auth/login/content/{kind}',
                load_trigger=PageEvent(name='tab'),
                components=await auth_login_content(kind, github_auth),
            ),
            title='Authentication',
        )
    else:
        return [c.FireEvent(event=GoToEvent(url='/auth/profile'))]


@router.get('/login/content/{kind}', response_model=FastUI, response_model_exclude_none=True)
async def auth_login_content(
    kind: LoginKind, github_auth: Annotated[GitHubAuthProvider, Depends(get_github_auth)]
) -> list[AnyComponent]:
    match kind:
        case 'password':
            return [
                c.Heading(text='Password Login', level=3),
                c.Paragraph(
                    text=(
                        'This is a very simple demo of password authentication, '
                        'here you can "login" with any email address and password.'
                    )
                ),
                c.Paragraph(text='(Passwords are not saved and email address are deleted after around an hour.)'),
                c.ModelForm(model=LoginForm, submit_url='/api/auth/login'),
            ]
        case 'github':
            auth_url = await github_auth.authorization_url()
            return [
                c.Heading(text='GitHub Login', level=3),
                c.Paragraph(text='Demo of GitHub authentication.'),
                c.Paragraph(text='(Credentials are deleted after around an hour.)'),
                c.Button(text='Login with GitHub', on_click=GoToEvent(url=auth_url)),
            ]
        case _:
            raise ValueError(f'Invalid kind {kind!r}')


class LoginForm(BaseModel):
    email: EmailStr = Field(title='Email Address', description='Enter whatever value you like')
    password: SecretStr = Field(
        title='Password',
        description='Enter whatever value you like, password is not checked',
        json_schema_extra={'autocomplete': 'current-password'},
    )


@router.post('/login', response_model=FastUI, response_model_exclude_none=True)
async def login_form_post(form: Annotated[LoginForm, fastui_form(LoginForm)]) -> list[AnyComponent]:
    token = await db.create_user(form.email)
    return [c.FireEvent(event=AuthEvent(token=token, url='/auth/profile'))]


@router.get('/profile', response_model=FastUI, response_model_exclude_none=True)
async def profile(user: Annotated[db.User | None, Depends(get_user)]) -> list[AnyComponent]:
    if user is None:
        return [c.FireEvent(event=GoToEvent(url='/auth/login'))]
    else:
        active_count = await db.count_users()
        return demo_page(
            c.Paragraph(text=f'You are logged in as "{user.email}", {active_count} active users right now.'),
            c.Button(text='Logout', on_click=PageEvent(name='submit-form')),
            c.Form(
                submit_url='/api/auth/logout',
                form_fields=[c.FormFieldInput(name='test', title='', initial='data', html_type='hidden')],
                footer=[],
                submit_trigger=PageEvent(name='submit-form'),
            ),
            title='Authentication',
        )


@router.post('/logout', response_model=FastUI, response_model_exclude_none=True)
async def logout_form_post(user: Annotated[db.User | None, Depends(get_user)]) -> list[AnyComponent]:
    if user is not None:
        await db.delete_user(user)
    return [c.FireEvent(event=AuthEvent(token=False, url='/auth/login/password'))]


@router.get('/login/github/redirect', response_model=FastUI, response_model_exclude_none=True)
async def github_redirect(
    code: str,
    state: str | None,
    github_auth: Annotated[GitHubAuthProvider, Depends(get_github_auth)],
) -> list[AnyComponent]:
    try:
        exchange = await github_auth.exchange_code(code, state)
    except AuthError as e:
        return [c.Text(text=f'Error: {e}')]
    user_info = await github_auth.get_github_user(exchange)
    token = await db.create_user(user_info.email or user_info.username)
    return [c.FireEvent(event=AuthEvent(token=token, url='/auth/profile'))]
