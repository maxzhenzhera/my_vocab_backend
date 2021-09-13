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


class TokenInResponse(ModelWithOrmMode):
    token: str
    expires_at: datetime
    token_type: str = 'bearer'


class TokensInResponse(ModelWithOrmMode):
    access_token: TokenInResponse
    refresh_token: TokenInResponse
