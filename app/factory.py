from fastapi import FastAPI

from app.builder import AppBuilder
from app.core.config import get_app_settings
from app.core.settings import AppSettings


__all__ = ['get_app']


def get_app(settings: AppSettings | None = None) -> FastAPI:
    settings = settings or get_app_settings()
    return AppBuilder(settings).build()
