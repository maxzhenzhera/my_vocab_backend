from dataclasses import dataclass
from datetime import (
    datetime,
    timedelta
)

from jose import jwt

from .base import BaseUserService
from ..schemas.jwt import (
    JWTMeta,
    JWTUser
)
from ..core.config import jwt_config


__all__ = ['UserJWTService']


@dataclass
class TokenPayloadMetaClaims:
    expire_timedelta: timedelta
    subject: str


@dataclass
class TokenDataForEncoding:
    meta_claims: TokenPayloadMetaClaims
    secret: str


class UserJWTService(BaseUserService):
    @property
    def jwt_user(self) -> JWTUser:
        return JWTUser.from_orm(self.user)

    @staticmethod
    def verify_access_token(token: str) -> JWTUser:
        return JWTUser(**jwt.decode(token, jwt_config.ACCESS_TOKEN_SECRET_KEY, jwt_config.ALGORITHM))

    @staticmethod
    def verify_refresh_token(token: str) -> JWTUser:
        return JWTUser(**jwt.decode(token, jwt_config.REFRESH_TOKEN_SECRET_KEY, jwt_config.ALGORITHM))

    def generate_tokens(self):
        return self._generate_access_token(), self._generate_refresh_token()

    def _generate_access_token(self) -> str:
        return self._generate_token(
            TokenDataForEncoding(
                TokenPayloadMetaClaims(jwt_config.ACCESS_TOKEN_EXPIRE_TIMEDELTA, jwt_config.ACCESS_TOKEN_SUBJECT),
                jwt_config.ACCESS_TOKEN_SECRET_KEY
            )
        )

    def _generate_refresh_token(self) -> str:
        return self._generate_token(
            TokenDataForEncoding(
                TokenPayloadMetaClaims(jwt_config.REFRESH_TOKEN_EXPIRE_TIMEDELTA, jwt_config.REFRESH_TOKEN_SUBJECT),
                jwt_config.REFRESH_TOKEN_SECRET_KEY
            )
        )

    def _generate_token(self, token_data: TokenDataForEncoding) -> str:
        return jwt.encode(self._prepare_payload(token_data.meta_claims), token_data.secret, jwt_config.ALGORITHM)

    def _prepare_payload(self, meta_claims: TokenPayloadMetaClaims) -> dict:
        return self._make_user_payload() | self._make_meta_payload(meta_claims)

    def _make_user_payload(self) -> dict:
        return self.jwt_user.dict()

    def _make_meta_payload(self, meta_claims: TokenPayloadMetaClaims) -> dict:
        return JWTMeta(exp=self._compute_expire(meta_claims.expire_timedelta), sub=meta_claims.subject).dict()

    @staticmethod
    def _compute_expire(expire_timedelta: timedelta) -> datetime:
        return datetime.utcnow() + expire_timedelta
