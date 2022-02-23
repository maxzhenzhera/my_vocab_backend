from os import environ

from app.core.settings.environments import AppEnvironmentType


__all__ = ['set_app_environment']


def set_app_environment(env_type: AppEnvironmentType) -> None:
    environ['APP_ENV'] = env_type.value
