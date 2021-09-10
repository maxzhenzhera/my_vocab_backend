from datetime import datetime

from pydantic import BaseModel

from .base import ModelWithOrmMode


__all__ = [
    'JWTMeta',
    'JWTUser',
    'Tokens'
]


class JWTMeta(BaseModel):
    exp: datetime
    sub: str


class JWTUser(ModelWithOrmMode):
    email: str
    is_superuser: bool


class Tokens:
    access_token: str
    refresh_token: str
