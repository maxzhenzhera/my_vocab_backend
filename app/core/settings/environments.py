from enum import Enum
from typing import NewType


__all__ = [
    'AppEnvironmentType',
    'ENV_FILES'
]


EnvFileName = NewType('EnvFileName', str)


class AppEnvironmentType(str, Enum):
    PROD = 'prod'
    DEV = 'dev'
    TEST = 'test'


ENV_FILES: dict[AppEnvironmentType, EnvFileName] = {
    environment: EnvFileName(environment.value + '.env')
    for environment in AppEnvironmentType
}
