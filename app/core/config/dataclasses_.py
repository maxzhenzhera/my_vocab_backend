from dataclasses import (
    dataclass,
    field
)
from datetime import timedelta

from jose import jwt

from .paths import LOGGING_CONFIG_PATH


__all__ = [
    'ServerConfig',
    'UvicornConfig',
    'DBConfig',
    'JWTConfig'
]


@dataclass
class ServerConfig:
    HOST: str
    PORT: int
    API_PREFIX: str


@dataclass
class UvicornConfig:
    SERVER_CONFIG: ServerConfig
    LOGGING_CONFIG_PATH: str = field(default=str(LOGGING_CONFIG_PATH), init=False)
    RELOAD: bool = field(default=True, init=False)

    def get_config(self) -> dict:
        return {
            'host': self.SERVER_CONFIG.HOST,
            'port': self.SERVER_CONFIG.PORT,
            'log_config': self.LOGGING_CONFIG_PATH,
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
    ACCESS_TOKEN_SECRET_KEY: str
    REFRESH_TOKEN_SECRET_KEY: str
    ACCESS_TOKEN_TYPE: str = field(default='bearer', init=False)
    REFRESH_TOKEN_TYPE: str = field(default='refresh', init=False)
    ACCESS_TOKEN_SUBJECT: str = field(default='access', init=False)
    REFRESH_TOKEN_SUBJECT: str = field(default='refresh', init=False)
    ACCESS_TOKEN_EXPIRE_TIMEDELTA: timedelta = field(default=timedelta(minutes=30), init=False)
    REFRESH_TOKEN_EXPIRE_TIMEDELTA: timedelta = field(default=timedelta(weeks=1), init=False)
    ALGORITHM: str = field(default=jwt.ALGORITHMS.HS256, init=False)
