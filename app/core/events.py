from collections.abc import (
    Callable,
    Coroutine
)
from typing import (
    Any,
    TypeAlias
)

from fastapi import FastAPI

from .settings import AppSettings
from ..db.events import (
    close_db,
    init_db
)
from ..services.authentication.oauth.events import init_oauth
from ..services.mail.events import init_mail


__all__ = [
    'get_startup_handler',
    'get_shutdown_handler'
]


EventHandler: TypeAlias = Callable[[], Coroutine[Any, Any, None]]


def get_startup_handler(app: FastAPI, settings: AppSettings) -> EventHandler:
    async def start_app() -> None:
        init_db(app, settings.db)
        init_mail(app, settings.mail)
        init_oauth(app, settings.oauth)

    return start_app


def get_shutdown_handler(app: FastAPI) -> EventHandler:
    async def shutdown_app() -> None:
        await close_db(app)

    return shutdown_app
