from datetime import datetime
from typing import ClassVar

from sqlalchemy import (
    Boolean,
    update as sa_update
)
from sqlalchemy.sql import ColumnElement

from .base import BaseRepo
from ..models import User


__all__ = ['UsersRepo']


class UsersRepo(BaseRepo[User]):
    model: ClassVar = User

    async def fetch_by_id(self, id_: int) -> User:
        return await self._fetch_where(User.id == id_)

    async def fetch_by_email(self, email: str) -> User:
        return await self._fetch_where(User.email == email)

    async def check_email_is_taken(self, email: str) -> bool:
        return await self._exists_where(User.email == email)

    async def confirm_by_email(self, email: str) -> User:
        return await self._confirm_where(User.email == email)

    async def confirm_by_token(self, token: str) -> User:
        return await self._confirm_where(User.email_confirmation_token == token)

    async def _confirm_where(self, where_stmt: ColumnElement[Boolean]) -> User:
        stmt = (
            sa_update(User)
            .where(where_stmt)
            .values(
                is_email_confirmed=True,
                email_confirmed_at=datetime.utcnow()
            )
        )
        result = await self._return_from_statement(stmt)
        return self._get_entity_or_raise(result)
