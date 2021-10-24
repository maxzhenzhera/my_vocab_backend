from datetime import (
    datetime,
    timedelta
)

from sqlalchemy import (
    delete as sa_delete,
    update as sa_update
)
from sqlalchemy.future import select as sa_select

from .base import BaseRepository
from ..models import RefreshSession


__all__ = ['RefreshSessionsRepository']


class RefreshSessionsRepository(BaseRepository):
    model = RefreshSession

    async def fetch_by_refresh_token(self, refresh_token: str) -> RefreshSession:
        stmt = sa_select(RefreshSession).where(RefreshSession.refresh_token == refresh_token)
        return await self._fetch_entity(stmt)

    async def delete_by_refresh_token(self, refresh_token: str) -> RefreshSession:
        stmt = sa_delete(RefreshSession).where(RefreshSession.refresh_token == refresh_token)
        return await self._return_from_statement(stmt)

    async def expire(self, refresh_token: str) -> None:
        update_data = self._get_update_data_on_expire()
        async with self._session.begin_nested():
            stmt = sa_update(RefreshSession).where(RefreshSession.refresh_token == refresh_token).values(**update_data)
            await self._session.execute(stmt)

    @staticmethod
    def _get_update_data_on_expire() -> dict:
        return {
            'expires_at': datetime.utcnow() - timedelta(seconds=5)
        }
