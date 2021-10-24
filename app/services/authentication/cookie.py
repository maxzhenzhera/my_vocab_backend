from dataclasses import dataclass
from datetime import timedelta
from pathlib import PurePosixPath as URLPathJoiner

from fastapi import Response

from ...core.config.config import (
    server_config,
    refresh_session_config
)


__all__ = [
    'CookieService',
    'REFRESH_TOKEN_COOKIE_KEY'
]


REFRESH_TOKEN_COOKIE_KEY = 'refresh_token'


@dataclass
class CookieService:
    response: Response

    @property
    def refresh_token_path(self) -> str:
        return str(URLPathJoiner(server_config.API_PREFIX, 'auth'))

    @property
    def refresh_token_cookie_max_age(self) -> int:
        return self._get_total_seconds_of_timedelta(refresh_session_config.REFRESH_TOKEN_EXPIRE_TIMEDELTA)

    @staticmethod
    def _get_total_seconds_of_timedelta(delta: timedelta) -> int:
        return int(delta.total_seconds())

    def set_refresh_token(self, refresh_token: str) -> None:
        self.response.set_cookie(
            key=REFRESH_TOKEN_COOKIE_KEY,
            value=refresh_token,
            max_age=self.refresh_token_cookie_max_age,
            path=self.refresh_token_path,
            httponly=True
        )

    def delete_refresh_token(self) -> None:
        self.response.delete_cookie(
            key=REFRESH_TOKEN_COOKIE_KEY,
            path=self.refresh_token_path,
        )
