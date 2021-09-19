from typing import Callable

from fastapi import FastAPI

from ..db.events import (
    init_db,
    close_db
)


__all__ = [
    'get_startup_handler',
    'get_shutdown_handler'
]


def get_startup_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        init_db(app)

    return start_app


def get_shutdown_handler(app: FastAPI) -> Callable:
    async def shutdown_app() -> None:
        await close_db(app)

    return shutdown_app
