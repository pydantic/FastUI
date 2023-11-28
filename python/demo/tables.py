from datetime import date
from functools import cache
from pathlib import Path

from fastapi import APIRouter
from fastui import AnyComponent, Display, FastUI
from fastui import components as c
from fastui.events import GoToEvent
from pydantic import BaseModel, Field, TypeAdapter

from .shared import navbar

router = APIRouter()


def tabs() -> AnyComponent:
    return c.LinkList(
        links=[
            c.Link(
                components=[c.Text(text='Cities')],
                on_click=GoToEvent(url='/table'),
                active='/table',
            ),
            c.Link(
                components=[c.Text(text='Users')],
                on_click=GoToEvent(url='/table/users'),
                active='/table/users',
            ),
        ],
        mode='tabs',
        class_name='+ mb-4',
    )


class City(BaseModel):
    id: int = Field(title='ID')
    city: str = Field(title='Name')
    city_ascii: str = Field(title='City Ascii')
    lat: float = Field(title='Latitude')
    lng: float = Field(title='Longitude')
    country: str = Field(title='Country')
    iso2: str = Field(title='ISO2')
    iso3: str = Field(title='ISO3')
    admin_name: str | None = Field(title='Admin Name')
    capital: str | None = Field(title='Capital')
    population: float = Field(title='Population')


@cache
def get_cities() -> list[City]:
    cities_adapter = TypeAdapter(list[City])
    cities_file = Path(__file__).parent / 'cities.json'
    cities = cities_adapter.validate_json(cities_file.read_bytes())
    cities.sort(key=lambda city: city.population, reverse=True)
    return cities


@router.get('', response_model=FastUI, response_model_exclude_none=True)
def cities_view(page: int = 1) -> list[AnyComponent]:
    cities = get_cities()
    page_size = 50
    return [
        navbar(),
        c.PageTitle(text='FastUI Demo - Table'),
        c.Page(
            components=[
                c.Heading(text='Tables'),
                tabs(),
                c.Heading(text='Cities', level=3),
                c.Table[City](
                    data=cities[(page - 1) * page_size : page * page_size],
                    columns=[
                        c.TableColumn(field='city', on_click=GoToEvent(url='/more/{id}/'), width_percent=33),
                        c.TableColumn(field='country', width_percent=33),
                        c.TableColumn(field='population', width_percent=33),
                    ],
                ),
                c.Pagination(page=page, page_size=page_size, total=len(cities)),
            ]
        ),
    ]


class MyTableRow(BaseModel):
    id: int = Field(title='ID')
    name: str = Field(title='Name')
    dob: date = Field(title='Date of Birth')
    enabled: bool | None = None


@router.get('/users', response_model=FastUI, response_model_exclude_none=True)
def users_view() -> list[AnyComponent]:
    return [
        navbar(),
        c.PageTitle(text='FastUI Demo - Table'),
        c.Page(
            components=[
                c.Heading(text='Table'),
                tabs(),
                c.Heading(text='Users', level=3),
                c.Table[MyTableRow](
                    data=[
                        MyTableRow(id=1, name='John', dob=date(1990, 1, 1), enabled=True),
                        MyTableRow(id=2, name='Jane', dob=date(1991, 1, 1), enabled=False),
                        MyTableRow(id=3, name='Jack', dob=date(1992, 1, 1)),
                    ],
                    columns=[
                        c.TableColumn(field='name', on_click=GoToEvent(url='/more/{id}/')),
                        c.TableColumn(field='dob', display=Display.date),
                        c.TableColumn(field='enabled'),
                    ],
                ),
            ]
        ),
    ]
