from dataclasses import dataclass
from datetime import (
    datetime,
    timedelta
)


__all__ = [
    'TokenPayloadMetaClaims',
    'TokenDataForEncoding',
    'Token',
    'Tokens'
]


@dataclass
class TokenPayloadMetaClaims:
    expire_timedelta: timedelta
    subject: str


@dataclass
class TokenDataForEncoding:
    meta_claims: TokenPayloadMetaClaims
    secret: str


@dataclass
class Token:
    token: str
    expires_at: datetime


@dataclass
class Tokens:
    access_token: Token
    refresh_token: Token
