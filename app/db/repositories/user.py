from uuid import uuid4

from sqlalchemy import update as sa_update
from sqlalchemy.future import select as sa_select

from .base import BaseRepository
from ..errors import (
    EntityDoesNotExistError,
    EmailIsAlreadyTakenError
)
from ..models import User
from ...schemas.user import UserInUpdate
from ...services.security import UserPasswordService


__all__ = ['UsersRepository']


class UsersRepository(BaseRepository):
    model = User

    async def update(self, email: str, user_in_update: UserInUpdate) -> User:
        update_data = self._exclude_unset_from_schema(user_in_update)
        if 'email' in update_data:
            if await self.check_email_is_taken(update_data['email']):
                raise EmailIsAlreadyTakenError
            update_data.update(self._get_update_data_on_email_update())
        if 'password' in update_data:
            update_data.update(self._get_update_data_on_password_update(update_data['password']))
        stmt = sa_update(User).where(User.email == email).values(**update_data).returning(User)
        return await self._return_from_update(stmt)

    @staticmethod
    def _get_update_data_on_email_update() -> dict:
        return {
            'is_email_confirmed': False,
            'email_confirmed_at': None,
            'activation_link': uuid4()
        }

    @staticmethod
    def _get_update_data_on_password_update(password: str) -> dict:
        user = UserPasswordService(User()).change_password(password)
        return {
            'hashed_password': user.hashed_password,
            'password_salt': user.password_salt
        }

    async def fetch_by_email(self, email: str) -> User:
        stmt = sa_select(User).where(User.email == email)
        return await self._fetch_entity(stmt)

    async def check_email_is_taken(self, email: str) -> bool:
        try:
            _ = await self.fetch_by_email(email)
        except EntityDoesNotExistError:
            return False
        else:
            return True
