from dataclasses import dataclass
from typing import ClassVar

from fastapi import (
    Depends,
    Response
)

from ....api.dependencies.settings import AppSettingsMarker
from ....core.settings import AppSettings


__all__ = [
    'CookieService',
    'REFRESH_TOKEN_COOKIE_KEY'
]


REFRESH_TOKEN_COOKIE_KEY = 'refresh_token'


@dataclass
class CookieService:
    refresh_token_path: ClassVar[str] = '/api/auth'

    response: Response
    settings: AppSettings = Depends(AppSettingsMarker)

    @property
    def refresh_token_cookie_max_age(self) -> int:
        return self.settings.tokens.refresh.expire_in_seconds

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
