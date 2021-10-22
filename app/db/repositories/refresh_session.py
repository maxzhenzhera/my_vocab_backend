from sqlalchemy import delete as sa_delete
from sqlalchemy.future import select as sa_select

from .base import BaseRepository
from ..models import RefreshSession


__all__ = ['RefreshSessionsRepository']


class RefreshSessionsRepository(BaseRepository):
    model = RefreshSession

    async def fetch_by_refresh_token(self, refresh_token: str) -> RefreshSession:
        stmt = sa_select(RefreshSession).where(RefreshSession.refresh_token == refresh_token)
        return await self._fetch_entity(stmt)

    async def delete_by_refresh_token(self, refresh_token: str) -> None:
        async with self._session.begin_nested():
            stmt = sa_delete(RefreshSession).where(RefreshSession.refresh_token == refresh_token)
            await self._session.execute(stmt)
