import re

import pytest
from dirty_equals import IsList, IsStr
from fastapi.testclient import TestClient

from . import app

client = TestClient(app)


def test_index():
    r = client.get('/')
    assert r.status_code == 200, r.text
    assert r.text.startswith('<!doctype html>\n')
    assert r.headers.get('content-type') == 'text/html; charset=utf-8'


def test_api_root():
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
            'links': IsList(length=4),
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
    r = client.get('/api/')
    assert r.status_code == 200
    data = r.json()
    for link in data[1]['links']:
        url = link['onClick']['url']
        yield pytest.param(f'/api{url}', id=url)


@pytest.mark.parametrize('url', get_menu_links())
def test_menu_links(url: str):
    r = client.get(url)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)


# TODO tests for forms, including submission
