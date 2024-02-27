from __future__ import annotations as _annotations

from fastapi import APIRouter
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.components import RechartsLineChart
from fastui.events import PageEvent
from pydantic import BaseModel

from .shared import demo_page

router = APIRouter()


@router.get('/{kind}', response_model=FastUI, response_model_exclude_none=True)
def charts_view(kind: str) -> list[AnyComponent]:
    return demo_page(
        c.LinkList(
            links=[
                c.Link(
                    components=[c.Text(text='Recharts Line Chart')],
                    on_click=PageEvent(
                        name='change-chart',
                        push_path='/charts/recharts-line-chart',
                        context={'kind': 'recharts-line-chart'},
                    ),
                    active='/charts/recharts-line-chart',
                ),
            ],
            mode='tabs',
            class_name='+ mb-4',
        ),
        c.ServerLoad(
            path='/charts/content/{kind}',
            load_trigger=PageEvent(name='change-chart'),
            components=charts_content_view(kind),
        ),
        title='Charts',
    )


class Data(BaseModel):
    name: str
    uv: int
    pv: int
    amt: int


data_list = [
    Data(name='Page A', uv=4000, pv=2400, amt=2400),
    Data(name='Page B', uv=3000, pv=1398, amt=2210),
    Data(name='Page C', uv=2000, pv=9800, amt=2290),
    Data(name='Page D', uv=2780, pv=3908, amt=2000),
    Data(name='Page E', uv=1890, pv=4800, amt=2181),
    Data(name='Page F', uv=2390, pv=3800, amt=2500),
    Data(name='Page G', uv=3490, pv=4300, amt=2100),
]


@router.get('/content/{kind}', response_model=FastUI, response_model_exclude_none=True)
def charts_content_view(kind: str) -> list[AnyComponent]:
    match kind:
        case 'recharts-line-chart':
            return [
                c.Heading(text='Line chart', level=2),
                c.Paragraph(text='Line chart with Recharts.'),
                RechartsLineChart(
                    title='Recharts Line Chart',
                    width='100%',
                    height=300,
                    data=data_list,
                    x_key='name',
                    y_keys=['pv', 'uv', 'amt'],
                    y_keys_names=['Page Views', 'Unique Views', 'Amount'],
                    colors=['#8884d8', '#82ca9d', '#ffc658'],
                ),
            ]
        case _:
            return [c.Text(text='Unknown chart kind')]
