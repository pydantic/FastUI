"""
Simple tests of component creation.

NOTE: we do NOT want to exhaustively construct every component just for the same of it -
that's just testing pydantic!
"""
from fastui import components


def test_div_text():
    div = components.Div(components=[components.Text(text='hello world')])

    assert div.model_dump(by_alias=True, exclude_none=True) == {
        'components': [
            {
                'text': 'hello world',
                'type': 'Text',
            },
        ],
        'type': 'Div',
    }


def test_div_class_name():
    div = components.Div(components=[], class_name='foobar')

    assert div.model_dump(by_alias=True, exclude_none=True) == {
        'components': [],
        'className': 'foobar',
        'type': 'Div',
    }
