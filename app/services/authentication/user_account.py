from dataclasses import dataclass
from datetime import datetime

from fastapi import Depends

from .errors import (
    EmailIsAlreadyTakenRegistrationError,
    UserWithSuchEmailDoesNotExistError
)
from ..security import UserPasswordService
from ...api.dependencies.db import get_repository
from ...db.errors import EntityDoesNotExistError
from ...db.models import User
from ...db.repositories import UsersRepository
from ...schemas.authentication.oauth.user import OAuthUser
from ...schemas.entities.user import UserInCreate


__all__ = ['UserAccountService']


@dataclass
class UserAccountService:
    users_repository: UsersRepository = Depends(get_repository(UsersRepository))

    @staticmethod
    def generate_oauth_user_in_create(oauth_user: OAuthUser) -> UserInCreate:
        return UserInCreate(
            **oauth_user.dict(),
            password=UserPasswordService.generate_random_password()
        )

    async def register_user(self, user_in_create: UserInCreate) -> User:
        if await self.users_repository.check_email_is_taken(user_in_create.email):
            raise EmailIsAlreadyTakenRegistrationError(user_in_create.email)
        user = UserPasswordService(
            User(email=user_in_create.email)
        ).change_password(user_in_create.password)
        return await self.users_repository.create_by_entity(user)

    async def register_oauth_user(self, user_in_create: UserInCreate) -> User:
        if await self.users_repository.check_email_is_taken(user_in_create.email):
            raise EmailIsAlreadyTakenRegistrationError(user_in_create.email)
        user = UserPasswordService(
            User(
                email=user_in_create.email,
                is_email_confirmed=True,
                email_confirmed_at=datetime.utcnow()
            )
        ).change_password(user_in_create.password)
        return await self.users_repository.create_by_entity(user)

    async def fetch_user(self, email: str) -> User:
        try:
            user = await self.users_repository.fetch_by_email(email)
        except EntityDoesNotExistError as error:
            raise UserWithSuchEmailDoesNotExistError from error
        else:
            return user
