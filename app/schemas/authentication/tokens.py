from pydantic import BaseModel

from ...core.config import (
    jwt_config,
    refresh_session_config
)


__all__ = [
    'AccessTokenInResponse',
    'RefreshTokenInResponse',
    'TokensInResponse'
]


class TokenInResponse(BaseModel):
    token: str
    token_type: str
    ttl: int


class AccessTokenInResponse(TokenInResponse):
    token_type: str = jwt_config.ACCESS_TOKEN_TYPE
    ttl: int = int(jwt_config.ACCESS_TOKEN_EXPIRE_TIMEDELTA.total_seconds())


class RefreshTokenInResponse(TokenInResponse):
    token_type: str = refresh_session_config.REFRESH_TOKEN_TYPE
    ttl: int = int(refresh_session_config.REFRESH_TOKEN_EXPIRE_TIMEDELTA.total_seconds())


class TokensInResponse(BaseModel):
    access_token: AccessTokenInResponse
    refresh_token: RefreshTokenInResponse
