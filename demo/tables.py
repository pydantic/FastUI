from datetime import date
from functools import cache
from pathlib import Path

import pydantic
from fastapi import APIRouter
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.components.display import DisplayLookup, DisplayMode
from fastui.events import BackEvent, GoToEvent
from pydantic import BaseModel, Field, TypeAdapter

from .shared import demo_page

router = APIRouter()


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
def cities_list() -> list[City]:
    cities_adapter = TypeAdapter(list[City])
    cities_file = Path(__file__).parent / 'cities.json'
    cities = cities_adapter.validate_json(cities_file.read_bytes())
    cities.sort(key=lambda city: city.population, reverse=True)
    return cities


@cache
def cities_lookup() -> dict[id, City]:
    return {city.id: city for city in cities_list()}


class FilterForm(pydantic.BaseModel):
    country: str = Field(json_schema_extra={'search_url': '/api/forms/search', 'placeholder': 'Filter by Country...'})


@router.get('/cities', response_model=FastUI, response_model_exclude_none=True)
def cities_view(page: int = 1, country: str | None = None) -> list[AnyComponent]:
    cities = cities_list()
    page_size = 50
    filter_form_initial = {}
    if country:
        cities = [city for city in cities if city.iso3 == country]
        country_name = cities[0].country if cities else country
        filter_form_initial['country'] = {'value': country, 'label': country_name}
    return demo_page(
        *tabs(),
        c.ModelForm(
            model=FilterForm,
            submit_url='.',
            initial=filter_form_initial,
            method='GOTO',
            submit_on_change=True,
            display_mode='inline',
        ),
        c.Table(
            data=cities[(page - 1) * page_size : page * page_size],
            data_model=City,
            columns=[
                DisplayLookup(field='city', on_click=GoToEvent(url='./{id}'), table_width_percent=33),
                DisplayLookup(field='country', table_width_percent=33),
                DisplayLookup(field='population', table_width_percent=33),
            ],
        ),
        c.Pagination(page=page, page_size=page_size, total=len(cities)),
        title='Cities',
    )


@router.get('/cities/{city_id}', response_model=FastUI, response_model_exclude_none=True)
def city_view(city_id: int) -> list[AnyComponent]:
    city = cities_lookup()[city_id]
    return demo_page(
        *tabs(),
        c.Link(components=[c.Text(text='Back')], on_click=BackEvent()),
        c.Details(data=city),
        title=city.city,
    )


class User(BaseModel):
    id: int = Field(title='ID')
    name: str = Field(title='Name')
    dob: date = Field(title='Date of Birth')
    enabled: bool | None = None


users: list[User] = [
    User(id=1, name='John', dob=date(1990, 1, 1), enabled=True),
    User(id=2, name='Jane', dob=date(1991, 1, 1), enabled=False),
    User(id=3, name='Jack', dob=date(1992, 1, 1)),
]


@router.get('/users', response_model=FastUI, response_model_exclude_none=True)
def users_view() -> list[AnyComponent]:
    return demo_page(
        *tabs(),
        c.Table(
            data=users,
            columns=[
                DisplayLookup(field='name', on_click=GoToEvent(url='/table/users/{id}/')),
                DisplayLookup(field='dob', mode=DisplayMode.date),
                DisplayLookup(field='enabled'),
            ],
        ),
        title='Users',
    )


def tabs() -> list[AnyComponent]:
    return [
        c.LinkList(
            links=[
                c.Link(
                    components=[c.Text(text='Cities')],
                    on_click=GoToEvent(url='/table/cities'),
                    active='startswith:/table/cities',
                ),
                c.Link(
                    components=[c.Text(text='Users')],
                    on_click=GoToEvent(url='/table/users'),
                    active='startswith:/table/users',
                ),
            ],
            mode='tabs',
            class_name='+ mb-4',
        ),
    ]


@router.get('/users/{id}/', response_model=FastUI, response_model_exclude_none=True)
def user_profile(id: int) -> list[AnyComponent]:
    user: User | None = users[id - 1] if id <= len(users) else None
    return demo_page(
        *tabs(),
        c.Link(components=[c.Text(text='Back')], on_click=BackEvent()),
        c.Details(
            data=user,
            fields=[
                DisplayLookup(field='name'),
                DisplayLookup(field='dob', mode=DisplayMode.date),
                DisplayLookup(field='enabled'),
            ],
        ),
        title=user.name,
    )
