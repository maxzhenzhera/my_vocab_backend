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

from app.db.repos.base import BaseRepo
from app.db.models import RefreshSession


__all__ = ['RefreshSessionsRepo']


class RefreshSessionsRepo(BaseRepo[RefreshSession]):
    model: ClassVar = RefreshSession

    async def fetch_by_refresh_token(self, refresh_token: str) -> RefreshSession:
        stmt = (
            sa_select(RefreshSession)
            .where(RefreshSession.refresh_token == refresh_token)
        )
        return await self._fetch_entity(stmt)

    async def delete_by_refresh_token(self, refresh_token: str) -> RefreshSession:
        stmt = (
            sa_delete(RefreshSession)
            .where(RefreshSession.refresh_token == refresh_token)
        )
        return await self._return_from_statement(stmt)

    async def expire(self, refresh_token: str) -> None:
        async with self.session.begin_nested():
            stmt = (
                sa_update(RefreshSession)
                .where(RefreshSession.refresh_token == refresh_token)
                .values(expires_at=datetime.utcnow() - timedelta(seconds=5))
            )
            await self.session.execute(stmt)
