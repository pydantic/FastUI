import json
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, List, Tuple, Union

from pydantic import SecretStr

from .. import AnyComponent, FastUI, events
from .. import components as c

if TYPE_CHECKING:
    from fastapi import FastAPI, Request

__all__ = 'AuthError', 'AuthRedirect', 'fastapi_auth_exception_handling', 'StateProvider'


class AuthException(ABC, Exception):
    """
    Base exception for all auth-related errors.
    """

    @abstractmethod
    def response_data(self) -> Tuple[int, str]:
        pass


class AuthError(AuthException):
    def __init__(self, message: str, *, code: str):
        super().__init__(message)
        self.code = code

    def response_data(self) -> Tuple[int, str]:
        return 401, json.dumps({'detail': str(self)})


class AuthRedirect(AuthException):
    """
    Special exception which should cause a 345 HTTP response with location specified via JSON in the body.
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
    Register an exception handler for `AuthException` in a FastAPI app.
    """
    from fastapi.responses import Response

    @app.exception_handler(AuthException)
    def auth_exception_handler(_request: 'Request', e: AuthException) -> Response:
        status_code, body = e.response_data()
        return Response(body, media_type='application/json', status_code=status_code)


class StateProvider:
    """
    This is a simple state provider for the GitHub OAuth flow which uses a JWT to create an unguessable state.

    It's in shared in case it's useful for other OAuth providers.
    """

    def __init__(self, secret: SecretStr, max_age: timedelta = timedelta(minutes=5)):
        self._secret = secret
        self._max_age = max_age

    async def new_state(self) -> str:
        import jwt

        data = {'exp': datetime.now(tz=timezone.utc) + self._max_age}
        return jwt.encode(data, self._secret.get_secret_value(), algorithm='HS256')

    async def check_state(self, state: str) -> bool:
        import jwt

        try:
            jwt.decode(state, self._secret.get_secret_value(), algorithms=['HS256'])
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return False
        else:
            return True
