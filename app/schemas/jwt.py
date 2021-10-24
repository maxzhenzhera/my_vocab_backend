from datetime import datetime

from pydantic import BaseModel

from .base import ModelWithOrmMode


__all__ = [
    'JWTMeta',
    'JWTUser'
]


class JWTMeta(BaseModel):
    exp: datetime
    sub: str


class JWTUser(ModelWithOrmMode):
    email: str
    is_superuser: bool
