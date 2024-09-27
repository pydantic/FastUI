import pytest
from fastui import components
from fastui.components import display
from pydantic import BaseModel, Field, computed_field


class User(BaseModel):
    id: int
    name: str = Field(title='Name')

    @computed_field(title='Representation')
    @property
    def representation(self) -> str:
        return f'{self.id}: {self.name}'


users = [User(id=1, name='john'), User(id=2, name='jack')]


def test_table_no_columns():
    table = components.Table(data=users)

    # insert_assert(table.model_dump(by_alias=True, exclude_none=True))
    assert table.model_dump(by_alias=True, exclude_none=True) == {
        'data': [
            {'id': 1, 'name': 'john', 'representation': '1: john'},
            {'id': 2, 'name': 'jack', 'representation': '2: jack'},
        ],
        'columns': [
            {'field': 'id'},
            {'field': 'name', 'title': 'Name'},
            {'field': 'representation', 'title': 'Representation'},
        ],
        'type': 'Table',
    }


def test_table_columns():
    table = components.Table(
        data=users,
        columns=[
            display.DisplayLookup(field='id', title='ID'),
            display.DisplayLookup(field='name'),
            display.DisplayLookup(field='representation'),
        ],
    )

    # insert_assert(table.model_dump(by_alias=True, exclude_none=True))
    assert table.model_dump(by_alias=True, exclude_none=True) == {
        'data': [
            {'id': 1, 'name': 'john', 'representation': '1: john'},
            {'id': 2, 'name': 'jack', 'representation': '2: jack'},
        ],
        'columns': [
            {'title': 'ID', 'field': 'id'},
            {'title': 'Name', 'field': 'name'},
            {'title': 'Representation', 'field': 'representation'},
        ],
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
        'columns': [
            {'field': 'id'},
            {'title': 'Name', 'field': 'name'},
            {'title': 'Representation', 'field': 'representation'},
        ],
        'type': 'Table',
    }


def test_display_no_fields():
    d = components.Details(data=users[0])

    # insert_assert(d.model_dump(by_alias=True, exclude_none=True))
    assert d.model_dump(by_alias=True, exclude_none=True) == {
        'data': {'id': 1, 'name': 'john', 'representation': '1: john'},
        'fields': [
            {'field': 'id'},
            {'title': 'Name', 'field': 'name'},
            {'title': 'Representation', 'field': 'representation'},
        ],
        'type': 'Details',
    }


def test_display_fields():
    d = components.Details(
        data=users[0], fields=[display.DisplayLookup(field='id', title='ID'), display.DisplayLookup(field='name')]
    )

    # insert_assert(d.model_dump(by_alias=True, exclude_none=True))
    assert d.model_dump(by_alias=True, exclude_none=True) == {
        'data': {'id': 1, 'name': 'john', 'representation': '1: john'},
        'fields': [{'title': 'ID', 'field': 'id'}, {'title': 'Name', 'field': 'name'}],
        'type': 'Details',
    }


def test_details_with_display_lookup_and_display():
    d = components.Details(
        data=users[0],
        fields=[
            display.DisplayLookup(field='id', title='ID'),
            display.DisplayLookup(field='name'),
            display.Display(value='display value', title='Display Title'),
        ],
    )

    # insert_assert(d.model_dump(by_alias=True, exclude_none=True))
    assert d.model_dump(by_alias=True, exclude_none=True) == {
        'data': {'id': 1, 'name': 'john', 'representation': '1: john'},
        'fields': [
            {'title': 'ID', 'field': 'id'},
            {'title': 'Name', 'field': 'name'},
            {'title': 'Display Title', 'value': 'display value', 'type': 'Display'},
        ],
        'type': 'Details',
    }


def test_table_respect_computed_field_title():
    class Foo(BaseModel):
        id: int

        @computed_field(title='Foo Name')
        def name(self) -> str:
            return f'foo{self.id}'

    foos = [Foo(id=1)]
    table = components.Table(data=foos)

    # insert_assert(table.model_dump(by_alias=True, exclude_none=True))
    assert table.model_dump(by_alias=True, exclude_none=True) == {
        'data': [{'id': 1, 'name': 'foo1'}],
        'columns': [{'field': 'id'}, {'title': 'Foo Name', 'field': 'name'}],
        'type': 'Table',
    }


def test_details_respect_computed_field_title():
    class Foo(BaseModel):
        id: int

        @computed_field(title='Foo Name')
        def name(self) -> str:
            return f'foo{self.id}'

    foos = Foo(id=1)
    details = components.Details(data=foos)

    # insert_assert(table.model_dump(by_alias=True, exclude_none=True))
    assert details.model_dump(by_alias=True, exclude_none=True) == {
        'data': {'id': 1, 'name': 'foo1'},
        'fields': [{'field': 'id'}, {'title': 'Foo Name', 'field': 'name'}],
        'type': 'Details',
    }
