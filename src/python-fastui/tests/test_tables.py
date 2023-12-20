import pytest
from fastui import components
from fastui.components import display
from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    name: str = Field(title='Name')


users = [User(id=1, name='john'), User(id=2, name='jack')]


def test_table_no_columns():
    table = components.Table(data=users)

    # insert_assert(table.model_dump(by_alias=True, exclude_none=True))
    assert table.model_dump(by_alias=True, exclude_none=True) == {
        'data': [{'id': 1, 'name': 'john'}, {'id': 2, 'name': 'jack'}],
        'columns': [{'field': 'id'}, {'field': 'name', 'title': 'Name'}],
        'type': 'Table',
    }


def test_table_columns():
    table = components.Table(
        data=users, columns=[display.DisplayLookup(field='id', title='ID'), display.DisplayLookup(field='name')]
    )

    # insert_assert(table.model_dump(by_alias=True, exclude_none=True))
    assert table.model_dump(by_alias=True, exclude_none=True) == {
        'data': [{'id': 1, 'name': 'john'}, {'id': 2, 'name': 'jack'}],
        'columns': [{'title': 'ID', 'field': 'id'}, {'field': 'name', 'title': 'Name'}],
        'type': 'Table',
    }


def test_table_empty_no_data_model():
    with pytest.raises(ValueError, match='Value error, Cannot infer model from empty data'):
        components.Table(data=[])


def test_table_empty_data_model():
    table = components.Table(data=[], data_model=User)

    # insert_assert(table.model_dump(by_alias=True, exclude_none=True))
    assert table.model_dump(by_alias=True, exclude_none=True) == {
        'data': [],
        'columns': [{'field': 'id'}, {'title': 'Name', 'field': 'name'}],
        'type': 'Table',
    }
