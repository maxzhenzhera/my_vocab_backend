from dataclasses import dataclass

from fastapi import Depends

from .errors import (
    EmailIsAlreadyTakenRegistrationError,
    UserWithSuchEmailDoesNotExistError
)
from ...api.dependencies.db import get_repository
from ...db.errors import EntityDoesNotExistError
from ...db.models import User
from ...db.repositories import UsersRepository
from ...schemas.user import UserInCreate
from ...services.security import UserPasswordService


__all__ = ['UserAccountService']


@dataclass
class UserAccountService:
    users_repository: UsersRepository = Depends(get_repository(UsersRepository))

    async def create_user(self, user_in_create: UserInCreate) -> User:
        if await self.users_repository.check_email_is_taken(user_in_create.email):
            raise EmailIsAlreadyTakenRegistrationError(user_in_create.email)
        user = UserPasswordService(User(email=user_in_create.email)).change_password(user_in_create.password)
        return await self.users_repository.create_by_entity(user)

    async def fetch_user_by_email_or_raise_auth_error(self, email: str) -> User:
        try:
            user = await self.users_repository.fetch_by_email(email)
        except EntityDoesNotExistError as error:
            raise UserWithSuchEmailDoesNotExistError from error
        else:
            return user
