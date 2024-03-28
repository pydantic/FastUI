import json
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Tuple, Union

from .. import AnyComponent, FastUI, events
from .. import components as c

if TYPE_CHECKING:
    from fastapi import FastAPI

__all__ = 'AuthError', 'AuthRedirect', 'fastapi_auth_exception_handling'


class AuthException(ABC, Exception):
    """
    Base exception for all auth-related errors.
    """

    @abstractmethod
    def response_data(self) -> Tuple[int, str]:
        raise NotImplementedError


class AuthError(AuthException):
    def __init__(self, message: str, *, code: str):
        super().__init__(message)
        self.code = code

    def response_data(self) -> Tuple[int, str]:
        return 401, json.dumps({'detail': str(self)})


class AuthRedirect(AuthException):
    """
    Special exception which should cause a 345 HTTP response with a body containing
    FastUI components to redirect the user to a new page.
    """

    def __init__(self, path: str, message: Union[str, None] = None):
        super().__init__(f'Auth redirect to `{path}`' + (f': {message}' if message else ''))
        self.path = path
        self.message = message

    def response_data(self) -> Tuple[int, str]:
        components: List[AnyComponent] = [c.FireEvent(event=events.GoToEvent(url=self.path), message=self.message)]
        return 345, FastUI(root=components).model_dump_json(exclude_none=True)


def fastapi_auth_exception_handling(app: 'FastAPI') -> None:
    """
    Register an exception handler for any `AuthException` in a FastAPI app.
    """
    from fastapi import Request, Response

    @app.exception_handler(AuthException)
    def auth_exception_handler(_request: Request, e: AuthException) -> Response:
        status_code, body = e.response_data()
        return Response(body, media_type='application/json', status_code=status_code)
