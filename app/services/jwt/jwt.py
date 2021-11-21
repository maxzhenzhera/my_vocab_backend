from datetime import datetime

from jose import jwt

from ..base import BaseUserService
from ...core.config import jwt_config
from ...schemas.jwt import (
    JWTMeta,
    JWTUser
)


__all__ = ['UserJWTService']


class UserJWTService(BaseUserService):
    @property
    def jwt_user(self) -> JWTUser:
        return JWTUser.from_orm(self.user)

    @staticmethod
    def verify_access_token(access_token: str) -> JWTUser:
        return JWTUser(
            **jwt.decode(
                access_token,
                jwt_config.ACCESS_TOKEN_SECRET_KEY,
                jwt_config.ALGORITHM
            )
        )

    def generate_access_token(self) -> str:
        return jwt.encode(
            self._prepare_payload(),
            jwt_config.ACCESS_TOKEN_SECRET_KEY,
            jwt_config.ALGORITHM
        )

    def _prepare_payload(self) -> dict:
        return self._make_user_payload() | self._make_meta_payload()

    def _make_user_payload(self) -> dict:
        return self.jwt_user.dict()

    def _make_meta_payload(self) -> dict:
        return JWTMeta(exp=self._compute_expire(), sub=str(self.user.id)).dict()

    @staticmethod
    def _compute_expire() -> datetime:
        return datetime.utcnow() + jwt_config.ACCESS_TOKEN_EXPIRE_TIMEDELTA
