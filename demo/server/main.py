from __future__ import annotations as _annotations

from fastapi import FastAPI
from pydantic import RootModel

import components
from components import AnyComponent
from components.events import PageEvent, GoToEvent

app = FastAPI()


class FastUi(RootModel):
    root: AnyComponent


@app.get('/api/', response_model=FastUi, response_model_exclude_none=True)
def read_root() -> AnyComponent:
    return components.Container(
        children=[
            components.Row(children=[
                components.Col(children=[components.Text(text='Hello')]),
                components.Col(children=[components.Text(text='World')]),
                components.Col(children=[components.Button(text='Show Modal', on_click=PageEvent(name='modal'))]),
                components.Col(children=[components.Button(text='go to /foo', on_click=GoToEvent(url='/foo'))]),
            ]),
            components.Modal(
                title='Modal Title',
                body=[components.Text(text='Modal Content')],
                footer=[components.Button(text='Close', on_click=PageEvent(name='modal'))],
                open_trigger=PageEvent(name='modal'),
            ),
        ],
        class_name='+ mt-4'
    )
