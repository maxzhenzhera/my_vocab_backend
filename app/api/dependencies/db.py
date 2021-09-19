from typing import (
    Callable,
    Type
)

from fastapi import (
    Depends,
    Request
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from ...db.repositories import BaseRepository


__all__ = ['get_repository']


def _get_sessionmaker(request: Request) -> sessionmaker:
    return request.app.state.db_sessionmaker


async def _get_session(db_sessionmaker: sessionmaker = Depends(_get_sessionmaker)) -> AsyncSession:
    async with db_sessionmaker() as session, session.begin():
        yield session


def get_repository(repository_type: Type[BaseRepository]) -> Callable[[AsyncSession], BaseRepository]:
    def _get_repo(session: AsyncSession = Depends(_get_session)) -> BaseRepository:
        return repository_type(session)
    return _get_repo
