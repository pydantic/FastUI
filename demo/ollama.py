# ollama_sse.py

from __future__ import annotations as _annotations

from fastapi import APIRouter
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.events import PageEvent

from .shared import demo_page

router = APIRouter()


def panel(*components: AnyComponent) -> AnyComponent:
    return c.Div(class_name='col border rounded m-1 p-2 pb-3', components=list(components))


@router.get('', response_model=FastUI, response_model_exclude_none=True)
def components_view() -> list[AnyComponent]:
    return demo_page(
        c.Div(
            components=[
                c.Heading(text='Server Load SSE', level=2),
                c.Markdown(text=('`ServerLoad` can also be used to load content from ollama.\n\n' '')),
                c.Button(text='Load SSE content', on_click=PageEvent(name='server-load-sse')),
                c.Div(
                    components=[
                        c.ServerLoad(
                            path='/components/sse',
                            sse=True,
                            load_trigger=PageEvent(name='server-load-sse'),
                            components=[c.Text(text='before')],
                        ),
                    ],
                    class_name='my-2 p-2 border rounded',
                ),
            ],
            class_name='border-top mt-3 pt-1',
        ),
    )
