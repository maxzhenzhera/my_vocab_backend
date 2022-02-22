from dataclasses import dataclass
from typing import ClassVar

from fastapi import Response

from ....core.config import get_app_settings
from ....core.settings.dataclasses_.components import RefreshSessionSettings


__all__ = [
    'CookieService',
    'REFRESH_TOKEN_COOKIE_KEY'
]


REFRESH_TOKEN_COOKIE_KEY = 'refresh_token'


@dataclass
class CookieService:
    SETTINGS: ClassVar[RefreshSessionSettings] = get_app_settings().REFRESH_SESSION

    response: Response

    @property
    def refresh_token_path(self) -> str:
        return '/api/auth'

    @property
    def refresh_token_cookie_max_age(self) -> int:
        return self.SETTINGS.REFRESH_TOKEN_EXPIRE_IN_SECONDS

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
