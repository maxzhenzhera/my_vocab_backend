from dataclasses import dataclass

from app.schemas.authentication.oauth import (
    OAuthUser,
    BaseOAuthConnection,
    GoogleOAuthConnection
)
from app.schemas.entities.user import (
    UserInCreate,
    UserInLogin
)


__all__ = ['TestUser']


@dataclass
class TestUser:
    email: str
    password: str
    google_id: str

    @property
    def in_create(self) -> UserInCreate:
        return UserInCreate(email=self.email, password=self.password)       # noqa pydantic email validation

    @property
    def in_login(self) -> UserInLogin:
        return UserInLogin(email=self.email, password=self.password)        # noqa pydantic email validation

    @property
    def google_oauth_user(self) -> OAuthUser:
        return OAuthUser(id=self.google_id, email=self.email)  # noqa pydantic email validation

    def get_oauth_connections(self, user_id: int) -> list[BaseOAuthConnection]:
        return [
            self.get_google_oauth_connection(user_id),
        ]

    def get_google_oauth_connection(self, user_id: int) -> GoogleOAuthConnection:
        return GoogleOAuthConnection(user_id=user_id, google_id=self.google_id)
