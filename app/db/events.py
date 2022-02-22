import logging

from fastapi import FastAPI

from .state import DBState
from ..core.settings.dataclasses_.components import DBSettings


__all__ = [
    'init_db',
    'close_db'
]


logger = logging.getLogger(__name__)


def init_db(app: FastAPI, settings: DBSettings) -> None:
    app.state.db = DBState(settings)
    logger.info('Database state (engine and sessionmaker) has been set.')


async def close_db(app: FastAPI) -> None:
    await app.state.db.engine.dispose()
    logger.info('Database engine has been disposed.')
