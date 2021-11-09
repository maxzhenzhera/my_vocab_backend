from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import ClassVar

from jose import jwt


__all__ = [
    'ServerConfig',
    'UvicornConfig',
    'DBConfig',
    'JWTConfig',
    'RefreshSessionConfig'
]


@dataclass
class ServerConfig:
    HOST: str
    PORT: int
    API_PREFIX: str


@dataclass
class UvicornConfig:
    SERVER_CONFIG: ServerConfig
    LOGGING_CONFIG_PATH: Path
    RELOAD: bool

    def get_run_config(self) -> dict:
        return {
            'host': self.SERVER_CONFIG.HOST,
            'port': self.SERVER_CONFIG.PORT,
            'log_config': str(self.LOGGING_CONFIG_PATH),
            'reload': self.RELOAD
        }


@dataclass
class DBConfig:
    HOST: str
    PORT: int
    NAME: str
    USER: str
    PASSWORD: str
    ENGINE: str = 'postgresql'
    DRIVER: str = 'asyncpg'

    @property
    def sqlalchemy_connection_string(self) -> str:
        return f'{self.ENGINE}+{self.DRIVER}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}'


@dataclass
class JWTConfig:
    ACCESS_TOKEN_TYPE: ClassVar[str] = 'Bearer'
    ACCESS_TOKEN_EXPIRE_TIMEDELTA: ClassVar[timedelta] = timedelta(minutes=30)
    ALGORITHM: ClassVar[str] = jwt.ALGORITHMS.HS256

    ACCESS_TOKEN_SECRET_KEY: str


@dataclass
class RefreshSessionConfig:
    REFRESH_TOKEN_TYPE: ClassVar[str] = 'Refresh'
    REFRESH_TOKEN_EXPIRE_TIMEDELTA: ClassVar[timedelta] = timedelta(weeks=1)
