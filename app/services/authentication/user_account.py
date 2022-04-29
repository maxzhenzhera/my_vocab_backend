from dataclasses import dataclass
from datetime import datetime

from fastapi import Depends

from .errors import (
    EmailIsAlreadyTakenError,
    UserWithSuchEmailDoesNotExistError
)
from .oauth.dataclasses_ import (
    OAuthUser,
    OAuthUserCredentials
)
from ..password import PasswordService
from ...api.dependencies.settings import AppSettingsMarker
from ...core.settings import AppSettings
from ...db.errors import EntityDoesNotExistError
from ...db.models import User
from ...db.repos import UsersRepo
from ...schemas.entities.user import UserInCreate


__all__ = ['UserAccountService']


@dataclass
class UserAccountService:
    settings: AppSettings = Depends(AppSettingsMarker)
    users_repo: UsersRepo = Depends()

    async def register_user(self, user_in_create: UserInCreate) -> User:
        return await self._create_user(
            user=User(email=user_in_create.email),
            password=user_in_create.password
        )

    async def register_oauth_user(
            self,
            oauth_user: OAuthUser
    ) -> tuple[User, OAuthUserCredentials]:
        credentials = self._form_oauth_user_credentials(oauth_user)
        return (
            await self._create_user(
                user=User(
                    email=credentials.email,
                    is_email_confirmed=True,
                    email_confirmed_at=datetime.utcnow()
                ),
                password=credentials.password
            ),
            credentials
        )

    @staticmethod
    def _form_oauth_user_credentials(oauth_user: OAuthUser) -> OAuthUserCredentials:
        return OAuthUserCredentials(
            email=oauth_user.email,
            password=PasswordService.generate_random_password()
        )

    async def _create_user(self, user: User, password: str) -> User:
        if await self.users_repo.check_email_is_taken(user.email):
            raise EmailIsAlreadyTakenError(user.email)
        PasswordService(user).set(password)
        return await self.users_repo.create_by_entity(user)

    async def fetch_by_email(self, email: str) -> User:
        try:
            user = await self.users_repo.fetch_by_email(email)
        except EntityDoesNotExistError as error:
            raise UserWithSuchEmailDoesNotExistError from error
        else:
            return user

    async def fetch_by_id(self, id_: int) -> User:
        """ Shortcut for using in the server authentication refresh. """
        return await self.users_repo.fetch_by_id(id_)

    async def confirm_email(self, user: User) -> User:
        if user.is_email_confirmed:
            return user
        return await self.users_repo.confirm_by_email(user.email)
