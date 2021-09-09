from sqlalchemy.ext.asyncio import AsyncSession

from ...db.session import db_sessionmaker


async def _get_session() -> AsyncSession:
    async with db_sessionmaker() as session, session.begin():
        yield session
