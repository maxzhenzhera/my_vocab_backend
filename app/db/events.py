import logging

from fastapi import FastAPI

from .postgres import (
    create_engine,
    create_sessionmaker
)
from ..core.config import sqlalchemy_connection_string


__all__ = [
    'init_db',
    'close_db'
]


logger = logging.getLogger(__name__)


def init_db(app: FastAPI) -> None:
    _set_db_in_app(sqlalchemy_connection_string, app)
    logger.info('Database engine and sessionmaker have been set.')


def _set_db_in_app(connection_string: str, app: FastAPI) -> None:
    app.state.db_engine = create_engine(connection_string)
    app.state.db_sessionmaker = create_sessionmaker(app.state.db_engine)


async def close_db(app: FastAPI) -> None:
    await app.state.db_engine.dispose()
    logger.info('Database engine has been disposed.')
