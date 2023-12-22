from __future__ import annotations as _annotations

from fastui import AnyComponent
from fastui import components as c
from fastui.events import GoToEvent


def demo_page(*components: AnyComponent, title: str | None = None) -> list[AnyComponent]:
    return [
        c.PageTitle(text=f'FastUI Demo — {title}' if title else 'FastUI Demo'),
        c.Navbar(
            title='FastUI Demo',
            title_event=GoToEvent(url='/'),
            links=[
                c.Link(
                    components=[c.Text(text='Components')],
                    on_click=GoToEvent(url='/components'),
                    active='startswith:/components',
                ),
                c.Link(
                    components=[c.Text(text='Tables')],
                    on_click=GoToEvent(url='/table/cities'),
                    active='startswith:/table',
                ),
                c.Link(
                    components=[c.Text(text='Auth')],
                    on_click=GoToEvent(url='/auth/login'),
                    active='startswith:/auth',
                ),
                c.Link(
                    components=[c.Text(text='Forms')],
                    on_click=GoToEvent(url='/forms/login'),
                    active='startswith:/forms',
                ),
            ],
        ),
        c.Page(
            components=[
                *((c.Heading(text=title),) if title else ()),
                *components,
            ],
        ),
        c.Footer(
            extra_text='FastUI Demo',
            links=[
                c.Link(
                    components=[c.Text(text='Github')], on_click=GoToEvent(url='https://github.com/pydantic/FastUI')
                ),
                c.Link(components=[c.Text(text='PyPI')], on_click=GoToEvent(url='https://pypi.org/project/fastui/')),
                c.Link(components=[c.Text(text='NPM')], on_click=GoToEvent(url='https://www.npmjs.com/org/pydantic/')),
            ],
        ),
    ]
