from __future__ import annotations as _annotations

import asyncio
import json
import os
from dataclasses import asdict
from typing import Annotated, Literal, TypeAlias

from fastapi import APIRouter, Depends, Request
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.auth import GitHubAuthProvider
from fastui.events import AuthEvent, GoToEvent, PageEvent
from fastui.forms import fastui_form
from httpx import AsyncClient
from pydantic import BaseModel, EmailStr, Field, SecretStr

from .auth_user import User
from .shared import demo_page

router = APIRouter()


# this will give an error when making requests to GitHub, but at least the app will run
GITHUB_CLIENT_SECRET = SecretStr(os.getenv('GITHUB_CLIENT_SECRET', 'dummy-secret'))


async def get_github_auth(request: Request) -> GitHubAuthProvider:
    client: AsyncClient = request.app.state.httpx_client
    return GitHubAuthProvider(
        httpx_client=client,
        github_client_id='9eddf87b27f71f52194a',
        github_client_secret=GITHUB_CLIENT_SECRET,
        scopes=['user:email'],
    )


LoginKind: TypeAlias = Literal['password', 'github']


@router.get('/login/{kind}', response_model=FastUI, response_model_exclude_none=True)
async def auth_login(
    kind: LoginKind,
    user: Annotated[User | None, Depends(User.from_request)],
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
    user = User(email=form.email, extra={})
    token = user.encode_token()
    return [c.FireEvent(event=AuthEvent(token=token, url='/auth/profile'))]


@router.get('/profile', response_model=FastUI, response_model_exclude_none=True)
async def profile(user: Annotated[User | None, Depends(User.from_request)]) -> list[AnyComponent]:
    if user is None:
        return [c.FireEvent(event=GoToEvent(url='/auth/login'))]
    else:
        return demo_page(
            c.Paragraph(text=f'You are logged in as "{user.email}".'),
            c.Button(text='Logout', on_click=PageEvent(name='submit-form')),
            c.Heading(text='User Data:', level=3),
            c.Code(language='json', text=json.dumps(asdict(user), indent=2)),
            c.Form(
                submit_url='/api/auth/logout',
                form_fields=[c.FormFieldInput(name='test', title='', initial='data', html_type='hidden')],
                footer=[],
                submit_trigger=PageEvent(name='submit-form'),
            ),
            title='Authentication',
        )


@router.post('/logout', response_model=FastUI, response_model_exclude_none=True)
async def logout_form_post() -> list[AnyComponent]:
    return [c.FireEvent(event=AuthEvent(token=False, url='/auth/login/password'))]


@router.get('/login/github/redirect', response_model=FastUI, response_model_exclude_none=True)
async def github_redirect(
    code: str,
    state: str | None,
    github_auth: Annotated[GitHubAuthProvider, Depends(get_github_auth)],
) -> list[AnyComponent]:
    exchange = await github_auth.exchange_code(code, state)
    user_info, emails = await asyncio.gather(
        github_auth.get_github_user(exchange), github_auth.get_github_user_emails(exchange)
    )
    user = User(
        email=next((e.email for e in emails if e.primary and e.verified), None),
        extra={
            'github_user_info': user_info.model_dump(),
            'github_emails': [e.model_dump() for e in emails],
        },
    )
    token = user.encode_token()
    return [c.FireEvent(event=AuthEvent(token=token, url='/auth/profile'))]
