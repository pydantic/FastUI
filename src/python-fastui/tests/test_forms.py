from contextlib import asynccontextmanager
from io import BytesIO
from typing import List, Tuple, Union

import pytest
from fastapi import HTTPException
from fastui import components
from fastui.forms import FormFile, fastui_form
from pydantic import BaseModel
from starlette.datastructures import FormData, Headers, UploadFile
from typing_extensions import Annotated


class SimpleForm(BaseModel):
    name: str
    size: int = 4


class FakeRequest:
    """
    TODO replace this with httpx or similar maybe, perhaps this is sufficient
    """

    def __init__(self, form_data_list: List[Tuple[str, Union[str, UploadFile]]]):
        self._form_data = FormData(form_data_list)

    @asynccontextmanager
    async def form(self):
        yield self._form_data


def test_simple_form_fields():
    m = components.ModelForm[SimpleForm](submit_url='/foobar/')

    assert m.model_dump(by_alias=True, exclude_none=True) == {
        'submitUrl': '/foobar/',
        'method': 'POST',
        'type': 'ModelForm',
        'formFields': [
            {
                'name': 'name',
                'title': ['Name'],
                'required': True,
                'locked': False,
                'htmlType': 'text',
                'type': 'FormFieldInput',
            },
            {
                'name': 'size',
                'title': ['Size'],
                'initial': 4,
                'required': False,
                'locked': False,
                'htmlType': 'number',
                'type': 'FormFieldInput',
            },
        ],
    }


async def test_simple_form_submit():
    form_dep = fastui_form(SimpleForm)

    request = FakeRequest([('name', 'bar'), ('size', '123')])

    m = await form_dep.dependency(request)
    assert isinstance(m, SimpleForm)
    assert m.model_dump() == {'name': 'bar', 'size': 123}


async def test_simple_form_submit_repeat():
    form_dep = fastui_form(SimpleForm)

    request = FakeRequest([('name', 'bar'), ('size', '123'), ('size', '456')])

    with pytest.raises(HTTPException) as exc_info:
        await form_dep.dependency(request)

    # insert_assert(exc_info.value.detail)
    assert exc_info.value.detail == {
        'form': [{'type': 'int_type', 'loc': ('size',), 'msg': 'Input should be a valid integer'}]
    }


class FormWithNested(BaseModel):
    name: str

    class NestedForm(BaseModel):
        x: int

    nested: NestedForm


def test_w_nested_form_fields():
    m = components.ModelForm[FormWithNested](submit_url='/foobar/')

    # insert_assert(m.model_dump(by_alias=True, exclude_none=True))
    assert m.model_dump(by_alias=True, exclude_none=True) == {
        'submitUrl': '/foobar/',
        'method': 'POST',
        'type': 'ModelForm',
        'formFields': [
            {
                'name': 'name',
                'title': ['Name'],
                'required': True,
                'locked': False,
                'htmlType': 'text',
                'type': 'FormFieldInput',
            },
            {
                'name': 'nested.x',
                'title': ['NestedForm', 'X'],
                'required': True,
                'locked': False,
                'htmlType': 'number',
                'type': 'FormFieldInput',
            },
        ],
    }


async def test_w_nested_form_submit():
    form_dep = fastui_form(FormWithNested)

    request = FakeRequest([('name', 'bar'), ('nested.x', '123')])

    m = await form_dep.dependency(request)
    assert isinstance(m, FormWithNested)
    assert m.model_dump() == {'name': 'bar', 'nested': {'x': 123}}


class FormWithFile(BaseModel):
    profile_pic: Annotated[UploadFile, FormFile()]


def test_file():
    m = components.ModelForm[FormWithFile](submit_url='/foobar/')

    # insert_assert(m.model_dump(by_alias=True, exclude_none=True))
    assert m.model_dump(by_alias=True, exclude_none=True) == {
        'submitUrl': '/foobar/',
        'method': 'POST',
        'type': 'ModelForm',
        'formFields': [
            {
                'name': 'profile_pic',
                'title': ['Profile Pic'],
                'required': True,
                'locked': False,
                'multiple': False,
                'type': 'FormFieldFile',
            }
        ],
    }


async def test_file_submit():
    file = UploadFile(BytesIO(b'foobar'), size=6, filename='testing.txt')
    request = FakeRequest([('profile_pic', file)])

    m = await fastui_form(FormWithFile).dependency(request)
    assert m.model_dump() == {'profile_pic': file}


async def test_file_submit_repeat():
    file1 = UploadFile(BytesIO(b'foobar'), size=6, filename='testing1.txt')
    file2 = UploadFile(BytesIO(b'foobar'), size=6, filename='testing2.txt')
    request = FakeRequest([('profile_pic', file1), ('profile_pic', file2)])

    with pytest.raises(HTTPException) as exc_info:
        await fastui_form(FormWithFile).dependency(request)

    # insert_assert(exc_info.value.detail)
    assert exc_info.value.detail == {
        'form': [{'type': 'not_file', 'loc': ('profile_pic',), 'msg': 'Input is not a file'}]
    }


class FormWithFileConstraint(BaseModel):
    profile_pic: Annotated[UploadFile, FormFile(accept='image/*', max_size=16_000)]


def test_file_constrained():
    m = components.ModelForm[FormWithFileConstraint](submit_url='/foobar/')

    # insert_assert(m.model_dump(by_alias=True, exclude_none=True))
    assert m.model_dump(by_alias=True, exclude_none=True) == {
        'submitUrl': '/foobar/',
        'method': 'POST',
        'type': 'ModelForm',
        'formFields': [
            {
                'name': 'profile_pic',
                'title': ['Profile Pic'],
                'required': True,
                'locked': False,
                'multiple': False,
                'accept': 'image/*',
                'type': 'FormFieldFile',
            }
        ],
    }


async def test_file_constrained_submit():
    headers = Headers({'content-type': 'image/png'})
    file = UploadFile(BytesIO(b'foobar'), size=16_000, headers=headers)
    request = FakeRequest([('profile_pic', file)])

    m = await fastui_form(FormWithFileConstraint).dependency(request)
    assert m.model_dump() == {'profile_pic': file}


async def test_file_constrained_submit_filename():
    file = UploadFile(BytesIO(b'foobar'), size=16_000, filename='image.png')
    request = FakeRequest([('profile_pic', file)])

    m = await fastui_form(FormWithFileConstraint).dependency(request)
    assert m.model_dump() == {'profile_pic': file}


async def test_file_constrained_submit_too_big():
    headers = Headers({'content-type': 'image/png'})
    file = UploadFile(BytesIO(b'foobar'), size=16_001, filename='image.png', headers=headers)
    request = FakeRequest([('profile_pic', file)])

    with pytest.raises(HTTPException) as exc_info:
        await fastui_form(FormWithFileConstraint).dependency(request)

    # insert_assert(exc_info.value.detail)
    assert exc_info.value.detail == {
        'form': [
            {
                'type': 'file_too_big',
                'loc': ('profile_pic',),
                'msg': 'File size was 15.6KiB, exceeding maximum allowed size of 15.6KiB',
            }
        ]
    }


async def test_file_constrained_submit_wrong_type():
    headers = Headers({'content-type': 'text/plain'})
    file = UploadFile(BytesIO(b'foobar'), size=16, filename='testing.txt', headers=headers)
    request = FakeRequest([('profile_pic', file)])

    with pytest.raises(HTTPException) as exc_info:
        await fastui_form(FormWithFileConstraint).dependency(request)

    # insert_assert(exc_info.value.detail)
    assert exc_info.value.detail == {
        'form': [
            {
                'type': 'accept_mismatch',
                'loc': ('profile_pic',),
                'msg': (
                    'Uploaded file "testing.txt" with content type "text/plain" '
                    'does not match accept criteria "image/*"'
                ),
            }
        ]
    }


class FormMultipleFiles(BaseModel):
    files: Annotated[List[UploadFile], FormFile()]


def test_multiple_files():
    m = components.ModelForm[FormMultipleFiles](submit_url='/foobar/')

    # insert_assert(m.model_dump(by_alias=True, exclude_none=True))
    assert m.model_dump(by_alias=True, exclude_none=True) == {
        'submitUrl': '/foobar/',
        'method': 'POST',
        'type': 'ModelForm',
        'formFields': [
            {
                'name': 'files',
                'title': ['Files'],
                'required': True,
                'locked': False,
                'multiple': True,
                'type': 'FormFieldFile',
            }
        ],
    }


async def test_multiple_files_single():
    file = UploadFile(BytesIO(b'foobar'), size=16_000, filename='image.png')
    request = FakeRequest([('files', file)])

    m = await fastui_form(FormMultipleFiles).dependency(request)
    assert m.model_dump() == {'files': [file]}


async def test_multiple_files_multiple():
    file1 = UploadFile(BytesIO(b'foobar'), size=6, filename='image1.png')
    file2 = UploadFile(BytesIO(b'foobar'), size=6, filename='image2.png')
    request = FakeRequest([('files', file1), ('files', file2)])

    m = await fastui_form(FormMultipleFiles).dependency(request)
    assert m.model_dump() == {'files': [file1, file2]}
