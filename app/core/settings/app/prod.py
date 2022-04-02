from typing import ClassVar

from pydantic import Field

from .mixed import AppSettingsWithLogging
from ..dataclasses_.server import GunicornSettings


__all__ = ['AppProdSettings']


class AppProdSettings(AppSettingsWithLogging):
    gunicorn_worker_class: ClassVar[str] = 'uvicorn.workers.UvicornWorker'
    gunicorn_workers_number: int = Field(1, env='GUNICORN_WORKERS_NUMBER')

    @property
    def gunicorn(self) -> GunicornSettings:
        return GunicornSettings(
            worker_class=self.gunicorn_worker_class,
            workers=self.gunicorn_workers_number
        )
