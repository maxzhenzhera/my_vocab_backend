from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine
)
from sqlalchemy.orm import sessionmaker

from ..core.config import sqlalchemy_connection_string


engine = create_async_engine(sqlalchemy_connection_string)
db_sessionmaker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
