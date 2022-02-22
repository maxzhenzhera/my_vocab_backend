from typing import ClassVar

from sqlalchemy import (
    Boolean,
    update as sa_update
)
from sqlalchemy.future import select as sa_select
from sqlalchemy.sql import ColumnElement

from .update_data import (
    get_update_data_on_email_confirmation, get_update_data_on_email_update,
    get_update_data_on_password_update
)
from ..base import BaseRepo
from ...errors import (
    EmailInUpdateIsAlreadyTakenError,
    EntityDoesNotExistError
)
from ...models import User
from ....schemas.entities.user import UserInUpdate


__all__ = ['UsersRepo']


class UsersRepo(BaseRepo[User]):
    model: ClassVar = User

    async def confirm_by_email(self, email: str) -> User:
        return await self._confirm_where(User.email == email)

    async def confirm_by_link(self, link: str) -> User:
        return await self._confirm_where(User.email_confirmation_link == link)

    async def _confirm_where(self, where_statement: ColumnElement[Boolean]) -> User:
        update_data = get_update_data_on_email_confirmation()
        stmt = (
            sa_update(User)
            .where(where_statement)
            .values(**update_data)
        )
        return await self._return_from_statement(stmt)

    async def fetch_by_email(self, email: str) -> User:
        stmt = (
            sa_select(User)
            .where(User.email == email)
        )
        return await self._fetch_entity(stmt)

    async def fetch_by_id(self, id_: int) -> User:
        stmt = (
            sa_select(self.model)
            .where(self.model.id == id_)
        )
        return await self._fetch_entity(stmt)

    async def check_email_is_taken(self, email: str) -> bool:
        try:
            _ = await self.fetch_by_email(email)
        except EntityDoesNotExistError:
            return False
        else:
            return True
