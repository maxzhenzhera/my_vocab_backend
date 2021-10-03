from dataclasses import dataclass
from datetime import timedelta

from fastapi import Response

from ...core.config.config import jwt_config
from ...schemas.jwt import TokenInResponse


__all__ = ['CookieService']


@dataclass
class CookieService:
    response: Response

    @property
    def refresh_token_cookie_key(self) -> str:
        return 'refresh_token'

    @property
    def refresh_token_cookie_max_age(self) -> int:
        return self._get_total_seconds_of_timedelta(jwt_config.REFRESH_TOKEN_EXPIRE_TIMEDELTA)

    @staticmethod
    def _get_total_seconds_of_timedelta(delta: timedelta) -> int:
        return int(delta.total_seconds())

    def set_refresh_token(self, refresh_token: TokenInResponse) -> None:
        self.response.set_cookie(
            key=self.refresh_token_cookie_key,
            value=refresh_token.token,
            max_age=self.refresh_token_cookie_max_age,
            httponly=True
        )
