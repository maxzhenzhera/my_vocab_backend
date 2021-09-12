from datetime import datetime

from pydantic import BaseModel

from .base import ModelWithOrmMode


__all__ = [
    'JWTMeta',
    'JWTUser',
    'TokenInResponse',
    'TokensInResponse'
]


class JWTMeta(BaseModel):
    exp: datetime
    sub: str


class JWTUser(ModelWithOrmMode):
    email: str
    is_superuser: bool


class TokenInResponse(BaseModel):
    token: str
    token_type: str = 'bearer'


class TokensInResponse(BaseModel):
    access_token: TokenInResponse
    refresh_token: TokenInResponse
