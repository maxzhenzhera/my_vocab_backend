from dataclasses import dataclass

from app.schemas.entities.user import (
    UserInCreate,
    UserInLogin
)
from app.services.authentication.oauth.dataclasses_ import OAuthUser


__all__ = ['MetaUser']


@dataclass
class MetaUser:
    email: str
    password: str
    google_id: str

    @property
    def in_create(self) -> UserInCreate:
        return UserInCreate(
            email=self.email,
            password=self.password
        )

    @property
    def in_login(self) -> UserInLogin:
        return UserInLogin(
            email=self.email,
            password=self.password
        )

    @property
    def google_oauth_user(self) -> OAuthUser:
        return OAuthUser(
            id=self.google_id,
            email=self.email
        )
