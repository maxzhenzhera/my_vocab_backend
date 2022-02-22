import logging
from os import environ

from dotenv import (
    find_dotenv,
    load_dotenv
)

from .environments import (
    AppEnvironmentType,
    ENV_FILES
)


__all__ = [
    'recognize_app_environment_type',
    'load_app_environment'
]


logger = logging.getLogger(__name__)


def recognize_app_environment_type() -> AppEnvironmentType:
    load_dotenv()
    try:
        env_type = AppEnvironmentType(environ['APP_ENV'])
    except ValueError as error:
        env_types = ''.join(
            f'\n\t - {env_type!r}' for env_type in AppEnvironmentType
        )
        raise ValueError(
            f'Possible values for `APP_ENV` are: {env_types}'
        ) from error
    else:
        return env_type


def load_app_environment(env_type: AppEnvironmentType) -> None:
    load_dotenv(find_dotenv(ENV_FILES[env_type]))
    logger.info(f'{env_type!r} has been loaded.')
