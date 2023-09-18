from __future__ import annotations as _annotations

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class TextComponent(BaseModel, defer_build=True):
    type: Literal['Text'] = 'Text'
    text: str


class DivComponent(BaseModel, defer_build=True):
    type: Literal['Div'] = 'Div'
    children: list[AnyComp]


AnyComp = TextComponent | DivComponent
DivComponent.model_rebuild()

@app.get("/api/")
def read_root() -> AnyComp:
    return TextComponent(text="Hello World")
