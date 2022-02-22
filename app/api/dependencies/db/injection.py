from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from .markers import DBSessionInTransactionMarker
from ....builder import AppBuilder


__all__ = ['inject_db']


def inject_db(builder: AppBuilder) -> None:
    async def depend_on_db() -> AsyncGenerator[AsyncSession, None]:
        async with builder.app.state.db.sessionmaker() as session, session.begin():
            yield session

    builder.app.dependency_overrides[DBSessionInTransactionMarker] = depend_on_db
