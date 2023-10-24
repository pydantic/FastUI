from __future__ import annotations as _annotations

from typing import Literal, Any

from typing_extensions import TypedDict, Annotated, NotRequired

from fastapi import FastAPI
from pydantic import RootModel, Field, ConfigDict

app = FastAPI()
ClassName = Annotated[str | list[str] | dict[str, bool | None], Field(alias='className')]


def dict_not_none(**kwargs: Any) -> Any:
    return {k: v for k, v in kwargs.items() if v is not None}


class TextComp(TypedDict):
    type: Literal['Text']
    text: str


def text(text_: str) -> TextComp:
    return TextComp(type='Text', text=text_)


class DivComp(TypedDict):
    type: Literal['Div']
    children: list[AnyComp]
    class_name: NotRequired[ClassName]


def div(*children: AnyComp, class_name: ClassName | None = None) -> DivComp:
    return dict_not_none(type='Div', children=list(children), class_name=class_name)


class ContainerComp(TypedDict):
    type: Literal['Container']
    children: list[AnyComp]
    class_name: NotRequired[ClassName]


def container(*children: AnyComp, class_name: ClassName | None = None) -> ContainerComp:
    return dict_not_none(type='Container', children=list(children), class_name=class_name)


class RowComp(TypedDict):
    type: Literal['Row']
    children: list[AnyComp]
    class_name: NotRequired[ClassName]


def row(*children: AnyComp, class_name: ClassName | None = None) -> RowComp:
    return dict_not_none(type='Row', children=list(children), class_name=class_name)


class ColComp(TypedDict):
    type: Literal['Col']
    children: list[AnyComp]
    class_name: NotRequired[ClassName]


def col(*children: AnyComp, class_name: ClassName | None = None) -> ColComp:
    return dict_not_none(type='Col', children=list(children), class_name=class_name)


AnyComp = Annotated[TextComp | DivComp | ContainerComp | RowComp | ColComp, Field(discriminator='type')]


class FastUi(RootModel):
    model_config = ConfigDict(populate_by_name=True)
    root: AnyComp


@app.get("/api/", response_model=FastUi)
def read_root() -> AnyComp:
    return container(
        row(
            col(text("Hello")),
            col(text("World")),
        ),
        class_name='+ mt-4'
    )
