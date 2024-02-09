import json
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Annotated, Any, Self

import jwt
from fastapi import Header, HTTPException

JWT_SECRET = 'secret'


@dataclass
class User:
    email: str | None
    extra: dict[str, Any]

    def encode_token(self) -> str:
        return jwt.encode(asdict(self), JWT_SECRET, algorithm='HS256', json_encoder=CustomJsonEncoder)

    @classmethod
    async def from_request(cls, authorization: Annotated[str, Header()] = '') -> Self | None:
        try:
            token = authorization.split(' ', 1)[1]
        except IndexError:
            return None

        try:
            return cls(**jwt.decode(token, JWT_SECRET, algorithms=['HS256']))
        except jwt.DecodeError:
            raise HTTPException(status_code=401, detail='Invalid token')


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return super().default(obj)
