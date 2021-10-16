from datetime import datetime

from pydantic import BaseModel

from .base import ModelWithOrmMode
from ..core.config.config import jwt_config


__all__ = [
    'JWTMeta',
    'JWTUser',
    'AccessTokenInResponse',
    'RefreshTokenInResponse',
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
    token_type: str
    expires_at: datetime


class AccessTokenInResponse(TokenInResponse):
    token_type: str = jwt_config.ACCESS_TOKEN_TYPE


class RefreshTokenInResponse(TokenInResponse):
    token_type: str = jwt_config.REFRESH_TOKEN_TYPE


class TokensInResponse(ModelWithOrmMode):
    access_token: AccessTokenInResponse
    refresh_token: RefreshTokenInResponse
