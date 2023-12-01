from __future__ import annotations as _annotations

import asyncio
from datetime import datetime
from typing import AsyncIterable

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.events import GoToEvent, PageEvent

from .shared import demo_page

router = APIRouter()


def panel(*components: AnyComponent) -> AnyComponent:
    return c.Div(class_name='col border rounded m-1 p-2 pb-3', components=list(components))


@router.get('', response_model=FastUI, response_model_exclude_none=True)
def components_view() -> list[AnyComponent]:
    return demo_page(
        c.Div(
            components=[
                c.Heading(text='Text', level=2),
                c.Text(text='This is a text component.'),
            ]
        ),
        c.Div(
            components=[
                c.Heading(text='Paragraph', level=2),
                c.Paragraph(text='This is a paragraph component.'),
            ],
            class_name='border-top mt-3 pt-1',
        ),
        c.Div(
            components=[
                c.Heading(text='Heading', level=2),
                c.Heading(text='This is an H3', level=3),
                c.Heading(text='This is an H4', level=4),
            ],
            class_name='border-top mt-3 pt-1',
        ),
        c.Div(
            components=[
                c.Heading(text='Code', level=2),
                c.Code(
                    language='python',
                    text="""\
from pydantic import BaseModel

class Delivery(BaseModel):
    dimensions: tuple[int, int]

m = Delivery(dimensions=['10', '20'])
print(m.dimensions)
#> (10, 20)
""",
                ),
            ],
            class_name='border-top mt-3 pt-1',
        ),
        c.Div(
            components=[
                c.Heading(text='Link List', level=2),
                c.Markdown(
                    text=(
                        'This is a simple unstyled list of links, '
                        'LinkList is also used in `Navbar` and `Pagination`.'
                    )
                ),
                c.LinkList(
                    links=[
                        c.Link(
                            components=[c.Text(text='Internal Link - the the home page')],
                            on_click=GoToEvent(url='/'),
                        ),
                        c.Link(
                            components=[c.Text(text='Pydantic (External link)')],
                            on_click=GoToEvent(url='https://pydantic.dev'),
                        ),
                    ],
                ),
            ],
            class_name='border-top mt-3 pt-1',
        ),
        c.Div(
            components=[
                c.Heading(text='Button and Modal', level=2),
                c.Paragraph(text='The button below will open a modal with static content.'),
                c.Button(text='Show Static Modal', on_click=PageEvent(name='static-modal')),
                c.Modal(
                    title='Static Modal',
                    body=[c.Paragraph(text='This is some static content that was set when the modal was defined.')],
                    footer=[
                        c.Button(text='Close', on_click=PageEvent(name='static-modal', clear=True)),
                    ],
                    open_trigger=PageEvent(name='static-modal'),
                ),
            ],
            class_name='border-top mt-3 pt-1',
        ),
        c.Div(
            components=[
                c.Heading(text='Dynamic Modal', level=2),
                c.Markdown(
                    text=(
                        'The button below will open a modal with content loaded from the server when '
                        "it's opened using `ServerLoad`."
                    )
                ),
                c.Button(text='Show Dynamic Modal', on_click=PageEvent(name='dynamic-modal')),
                c.Modal(
                    title='Dynamic Modal',
                    body=[c.ServerLoad(path='/components/dynamic-content')],
                    footer=[
                        c.Button(text='Close', on_click=PageEvent(name='dynamic-modal', clear=True)),
                    ],
                    open_trigger=PageEvent(name='dynamic-modal'),
                ),
            ],
            class_name='border-top mt-3 pt-1',
        ),
        c.Div(
            components=[
                c.Heading(text='Server Load', level=2),
                c.Paragraph(text='Even simpler example of server load, replacing existing content.'),
                c.Button(text='Load Content from Server', on_click=PageEvent(name='server-load')),
                c.Div(
                    components=[
                        c.ServerLoad(
                            path='/components/dynamic-content',
                            load_trigger=PageEvent(name='server-load'),
                            components=[c.Text(text='before')],
                        ),
                    ],
                    class_name='py-2',
                ),
            ],
            class_name='border-top mt-3 pt-1',
        ),
        c.Div(
            components=[
                c.Heading(text='Server Load SSE', level=2),
                c.Markdown(text='`ServerLoad` can also be used to load content from an SSE stream.'),
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
        title='Components',
    )


@router.get('/dynamic-content', response_model=FastUI, response_model_exclude_none=True)
async def modal_view() -> list[AnyComponent]:
    await asyncio.sleep(0.5)
    return [c.Paragraph(text='This is some dynamic content. Open devtools to see me being fetched from the server.')]


async def sse_generator() -> AsyncIterable[str]:
    while True:
        d = datetime.now()
        m = FastUI(
            root=[
                c.Div(components=[c.Text(text=f'Time {d:%H:%M:%S}')], class_name='font-monospace'),
                c.Paragraph(text='This content is updated every second using an SSE stream.'),
            ]
        )
        yield f'data: {m.model_dump_json(by_alias=True)}\n\n'
        await asyncio.sleep(1)


@router.get('/sse')
async def sse_experiment() -> StreamingResponse:
    return StreamingResponse(sse_generator(), media_type='text/event-stream')
