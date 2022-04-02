import logging
from functools import cache
from typing import Final

from .settings import AppSettings
from .settings.app import (
    AppDevSettings,
    AppProdSettings,
    AppTestSettings
)
from .settings.environment import AppEnvType
from .settings.loader import (
    load_app_environment,
    recognize_app_environment_type
)


__all__ = ['get_app_settings']


logger = logging.getLogger(__name__)

ENVIRONMENTS: Final = {
    AppEnvType.PROD: AppProdSettings,
    AppEnvType.DEV: AppDevSettings,
    AppEnvType.TEST: AppTestSettings
}


@cache
def get_app_settings(env_type: AppEnvType | None = None) -> AppSettings:
    if env_type is not None:
        logger.debug(f'{env_type!r} has been passed programmatically.')
    else:
        env_type = recognize_app_environment_type()
    load_app_environment(env_type)
    return ENVIRONMENTS[env_type](env_type=env_type)  # type: ignore[no-any-return]
