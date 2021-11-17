from typing import (
    Callable,
    Type
)

from fastapi import (
    Depends,
    Request
)
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.repositories import BaseRepository


__all__ = ['get_repository']


def get_repository(repository_type: Type[BaseRepository]) -> Callable[[AsyncSession], BaseRepository]:
    def _get_repo(session: AsyncSession = Depends(_get_session)) -> BaseRepository:
        return repository_type(session)
    return _get_repo


async def _get_session(request: Request) -> AsyncSession:
    async with request.app.state.db_sessionmaker() as session, session.begin():
        yield session
