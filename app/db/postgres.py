from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine
)
from sqlalchemy.orm import sessionmaker


__all__ = [
    'create_engine',
    'create_sessionmaker'
]


def create_engine(sqlalchemy_connection_string: str) -> AsyncEngine:
    return create_async_engine(sqlalchemy_connection_string)


def create_sessionmaker(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
