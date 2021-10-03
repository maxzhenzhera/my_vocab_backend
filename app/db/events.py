import logging

from fastapi import FastAPI

from .postgres import (
    create_engine,
    create_sessionmaker
)
from ..core.config.config import sqlalchemy_connection_string


__all__ = [
    'init_db',
    'close_db'
]


logger = logging.getLogger(__name__)


def init_db(app: FastAPI) -> None:
    app.state.db_engine = create_engine(sqlalchemy_connection_string)
    app.state.db_sessionmaker = create_sessionmaker(app.state.db_engine)
    logger.info('Database engine and sessionmaker have been set.')


async def close_db(app: FastAPI) -> None:
    await app.state.db_engine.dispose()
    logger.info('Database engine has been disposed.')
