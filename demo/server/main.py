from __future__ import annotations as _annotations

from fastapi import FastAPI
from pydantic import RootModel

import components
from components import AnyComponent

app = FastAPI()


class FastUi(RootModel):
    root: AnyComponent


@app.get("/api/", response_model=FastUi)
def read_root() -> AnyComponent:
    return components.Container(
        children=[
            components.Row(children=[
                components.Col(children=[components.Text(text="Hello")]),
                components.Col(children=[components.Text(text="World")]),
            ])
        ],
        class_name='+ mt-4'
    )
