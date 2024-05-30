import re

import pytest
from dirty_equals import IsList, IsStr
from fastapi.testclient import TestClient

from . import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_index(client: TestClient):
    r = client.get('/')
    assert r.status_code == 200, r.text
    assert r.text.startswith('<!doctype html>\n')
    assert r.headers.get('content-type') == 'text/html; charset=utf-8'


def test_api_root(client: TestClient):
    r = client.get('/api/')
    assert r.status_code == 200
    data = r.json()
    assert data == [
        {
            'text': 'FastUI Demo',
            'type': 'PageTitle',
        },
        {
            'title': 'FastUI Demo',
            'titleEvent': {'url': '/', 'type': 'go-to'},
            'startLinks': IsList(length=4),
            'endLinks': [],
            'type': 'Navbar',
        },
        {
            'components': [
                {
                    'text': IsStr(regex='This site provides a demo of.*', regex_flags=re.DOTALL),
                    'type': 'Markdown',
                },
            ],
            'type': 'Page',
        },
        {
            'extraText': 'FastUI Demo',
            'links': IsList(length=3),
            'type': 'Footer',
        },
    ]


def get_menu_links():
    """
    This is pretty cursory, we just go through the menu and load each page.
    """
    with TestClient(app) as client:
        r = client.get('/api/')
        assert r.status_code == 200
        data = r.json()
        for link in data[1]['startLinks']:
            url = link['onClick']['url']
            yield pytest.param(f'/api{url}', id=url)


@pytest.mark.parametrize('url', get_menu_links())
def test_menu_links(client: TestClient, url: str):
    r = client.get(url)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)


# def test_forms_validate_correct_select_multiple(client: TestClient):
#     countries = client.get('api/forms/search', params={'q': None})
#     countries_options = countries.json()['options']
#     r = client.post(
#         'api/forms/select',
#         data={
#             'select_single': ToolEnum._member_names_[0],
#             'select_multiple': ToolEnum._member_names_[0],
#             'search_select_single': countries_options[0]['options'][0]['value'],
#             'search_select_multiple': countries_options[0]['options'][0]['value'],
#         },
#     )
#     assert r.status_code == 200


# TODO tests for forms, including submission
