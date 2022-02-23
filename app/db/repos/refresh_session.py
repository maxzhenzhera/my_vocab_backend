from datetime import (
    datetime,
    timedelta
)
from typing import ClassVar

from sqlalchemy import (
    delete as sa_delete,
    update as sa_update
)
from sqlalchemy.future import select as sa_select

from .base import BaseRepo
from ..models import RefreshSession


__all__ = ['RefreshSessionsRepo']


class RefreshSessionsRepo(BaseRepo[RefreshSession]):
    model: ClassVar = RefreshSession

    async def fetch_by_token(self, token: str) -> RefreshSession:
        stmt = (
            sa_select(RefreshSession)
            .where(RefreshSession.token == token)
        )
        return await self._fetch_entity(stmt)

    async def delete_by_token(self, token: str) -> RefreshSession | None:
        stmt = (
            sa_delete(RefreshSession)
            .where(RefreshSession.token == token)
        )
        result = await self._return_from_statement(stmt)
        return result.scalar()

    async def exists_by_token(self, token: str) -> bool:
        return await self._exists_where(RefreshSession.token == token)

    async def expire(
            self,
            token: str,
            *,
            expires_at: datetime | None = None
    ) -> None:
        expires_at = expires_at or datetime.utcnow() - timedelta(seconds=5)

        async with self.session.begin_nested():
            stmt = (
                sa_update(RefreshSession)
                .where(RefreshSession.token == token)
                .values(expires_at=expires_at)
            )
            await self.session.execute(stmt)
