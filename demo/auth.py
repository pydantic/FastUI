from __future__ import annotations as _annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Header
from pydantic import EmailStr, Field, SecretStr, BaseModel

from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.events import AuthEvent, GoToEvent
from fastui.forms import fastui_form

from .shared import demo_page

router = APIRouter()


def get_user(authorization: Annotated[str, Header()] = '') -> str | None:
    try:
        token = authorization.split(' ', 1)[1]
    except IndexError:
        return None
    else:
        return token


@router.get('/login', response_model=FastUI, response_model_exclude_none=True)
def auth_login(user: Annotated[str | None, Depends(get_user)]) -> list[AnyComponent]:
    if user is None:
        return demo_page(
            c.ModelForm[LoginForm](submit_url='/api/auth/login'),
            title='Authentication',
        )
    else:
        return [c.FireEvent(event=GoToEvent(url='/auth/profile'))]


class LoginForm(BaseModel):
    email: EmailStr = Field(title='Email Address', description="Enter whatever value you like")
    password: SecretStr = Field(
        title='Password',
        description='Enter whatever value you like, password is not checked',
        json_schema_extra={'autocomplete': 'current-password'}
    )


@router.post('/login', response_model=FastUI, response_model_exclude_none=True)
async def login_form_post(form: Annotated[LoginForm, fastui_form(LoginForm)]) -> list[AnyComponent]:
    print(form)
    return [c.FireEvent(event=AuthEvent(token=form.email, url='/auth/profile'))]


@router.get('/profile', response_model=FastUI, response_model_exclude_none=True)
def profile(user: Annotated[str | None, Depends(get_user)]) -> list[AnyComponent]:
    if user is None:
        return [c.FireEvent(event=GoToEvent(url='/auth/login'))]
    else:
        return demo_page(
            c.Paragraph(text=f"You are logged in as {user}"),
            c.Button(text='Logout', on_click=AuthEvent(token=False, url='/auth/login')),
            title='Authentication',
        )
