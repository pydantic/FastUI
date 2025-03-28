import json
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Dict, Generic, List, Tuple, TypeVar, Union

from .. import AnyComponent, FastUI, events
from .. import components as c

if TYPE_CHECKING:
    from fastapi import FastAPI


__all__ = 'AuthError', 'AuthRedirect', 'fastapi_auth_exception_handling', 'ExchangeCache', 'ExchangeData'


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


class ExchangeData:
    pass


T = TypeVar('T', bound='ExchangeData')


class ExchangeCache(Generic[T]):
    def __init__(self):
        self._data: Dict[str, Tuple[datetime, T]] = {}

    def get(self, key: str, max_age: timedelta) -> Union[T, None]:
        self._purge(max_age)
        if v := self._data.get(key):
            return v[1]

    def set(self, key: str, value: T) -> None:
        self._data[key] = (datetime.now(), value)

    def _purge(self, max_age: timedelta) -> None:
        """
        Remove old items from the exchange cache
        """
        min_timestamp = datetime.now() - max_age
        to_remove = [k for k, (ts, _) in self._data.items() if ts < min_timestamp]
        for k in to_remove:
            del self._data[k]

    def __len__(self) -> int:
        return len(self._data)

    def clear(self) -> None:
        self._data.clear()
