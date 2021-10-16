from dataclasses import dataclass
from datetime import timedelta
from pathlib import PurePosixPath as URLPathJoiner

from fastapi import Response

from ...core.config.config import (
    jwt_config,
    server_config
)
from ...schemas.jwt import RefreshTokenInResponse


__all__ = ['CookieService']


@dataclass
class CookieService:
    response: Response

    @property
    def refresh_token_cookie_key(self) -> str:
        return 'refresh_token'

    @property
    def refresh_token_path(self) -> str:
        return str(URLPathJoiner(server_config.API_PREFIX, 'auth'))

    @property
    def refresh_token_cookie_max_age(self) -> int:
        return self._get_total_seconds_of_timedelta(jwt_config.REFRESH_TOKEN_EXPIRE_TIMEDELTA)

    @staticmethod
    def _get_total_seconds_of_timedelta(delta: timedelta) -> int:
        return int(delta.total_seconds())

    def set_refresh_token(self, refresh_token: RefreshTokenInResponse) -> None:
        self.response.set_cookie(
            key=self.refresh_token_cookie_key,
            value=refresh_token.token,
            max_age=self.refresh_token_cookie_max_age,
            path=self.refresh_token_path,
            httponly=True
        )
