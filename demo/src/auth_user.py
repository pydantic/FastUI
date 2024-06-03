import json
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Annotated, Any

import jwt
from fastapi import Header, HTTPException
from fastui.auth import AuthRedirect
from typing_extensions import Self

JWT_SECRET = 'secret'


@dataclass
class User:
    email: str | None
    extra: dict[str, Any]

    def encode_token(self) -> str:
        payload = asdict(self)
        payload['exp'] = datetime.now() + timedelta(hours=1)
        return jwt.encode(payload, JWT_SECRET, algorithm='HS256', json_encoder=CustomJsonEncoder)

    @classmethod
    def from_request(cls, authorization: Annotated[str, Header()] = '') -> Self:
        user = cls.from_request_opt(authorization)
        if user is None:
            raise AuthRedirect('/auth/login/password')
        else:
            return user

    @classmethod
    def from_request_opt(cls, authorization: Annotated[str, Header()] = '') -> Self | None:
        try:
            token = authorization.split(' ', 1)[1]
        except IndexError:
            return None

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.DecodeError:
            raise HTTPException(status_code=401, detail='Invalid token')
        else:
            # existing token might not have 'exp' field
            payload.pop('exp', None)
            return cls(**payload)


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return super().default(obj)
