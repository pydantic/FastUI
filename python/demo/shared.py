from __future__ import annotations as _annotations

from fastui import AnyComponent
from fastui import components as c
from fastui.events import GoToEvent


def navbar() -> AnyComponent:
    return c.Navbar(
        title='FastUI Demo',
        links=[
            c.Link(components=[c.Text(text='Home')], on_click=GoToEvent(url='/'), active='/'),
            c.Link(components=[c.Text(text='Table')], on_click=GoToEvent(url='/table'), active='/table'),
            c.Link(components=[c.Text(text='Forms')], on_click=GoToEvent(url='/form/one'), active='startswith:/form'),
        ],
    )
