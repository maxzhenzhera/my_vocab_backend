from enum import Enum
from typing import Final


__all__ = [
    'AppEnvType',
    'ENV_FILES'
]


class AppEnvType(str, Enum):
    PROD = 'prod'
    DEV = 'dev'
    TEST = 'test'


ENV_FILES: Final = {
    environment: '.env.' + environment.value
    for environment in AppEnvType
}
