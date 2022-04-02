from collections.abc import Callable
from typing import Any

from fastapi import FastAPI
from gunicorn.app.base import BaseApplication


__all__ = ['StandaloneApplication']


class StandaloneApplication(BaseApplication):  # type: ignore[misc]
    def __init__(
            self,
            app: str | FastAPI | Callable[..., FastAPI],
            **kwargs: Any
    ) -> None:
        self.application = app
        self.options = kwargs

        super().__init__()

    def load_config(self) -> None:
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self) -> str | FastAPI | Callable[..., FastAPI]:
        return self.application
