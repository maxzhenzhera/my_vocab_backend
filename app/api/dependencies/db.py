from typing import (
    Callable,
    Type
)

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.repositories import BaseRepository
from ...db.session import db_sessionmaker


__all__ = ['get_repository']


async def _get_session() -> AsyncSession:
    async with db_sessionmaker() as session, session.begin():
        yield session


def get_repository(repository_type: Type[BaseRepository]) -> Callable[[AsyncSession], BaseRepository]:
    def _get_repo(session: AsyncSession = Depends(_get_session)) -> BaseRepository:
        return repository_type(session)
    return _get_repo
