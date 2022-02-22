from functools import cache

from .settings.builder import build_app_settings
from .settings.dataclasses_ import AppSettings
from .settings.helpers import (
    load_app_environment,
    recognize_app_environment_type
)


__all__ = ['get_app_settings']


@cache
def get_app_settings() -> AppSettings:
    env_type = recognize_app_environment_type()
    load_app_environment(env_type)
    return build_app_settings(env_type)
