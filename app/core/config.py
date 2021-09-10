from dataclasses import (
    dataclass,
    field
)
from datetime import timedelta
from pathlib import Path
from os import getenv

from dotenv import load_dotenv
from jose import jwt


__all__ = [
    'server_config',
    'uvicorn_config',
    'sqlalchemy_connection_string'
]


load_dotenv()


APP_DIR = Path(__file__).parent.parent
BASE_DIR = APP_DIR.parent
LOGGING_CONFIG_PATH = APP_DIR / 'utils' / 'logging_' / 'logging_config.yaml'


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
    ACCESS_TOKEN_SUBJECT: str = field(default='access', init=False)
    REFRESH_TOKEN_SUBJECT: str = field(default='refresh', init=False)
    ACCESS_TOKEN_EXPIRE_IN: timedelta = field(default=timedelta(minutes=30), init=False)
    REFRESH_TOKEN_EXPIRE_IN_MINUTES: timedelta = field(default=timedelta(weeks=1), init=False)
    ALGORITHM: str = field(default=jwt.ALGORITHMS.HS256, init=False)


server_config = ServerConfig(
    getenv('SERVER_HOST'),
    int(getenv('SERVER_PORT')),
    getenv('API_PREFIX', '/api')
)
uvicorn_config = UvicornConfig(
    server_config
).get_config()
sqlalchemy_connection_string = DBConfig(
    getenv('DB_HOST'),
    int(getenv('DB_PORT')),
    getenv('DB_NAME'),
    getenv('DB_USER'),
    getenv('DB_PASSWORD'),
).sqlalchemy_connection_string
jwt_config = JWTConfig(
    ACCESS_TOKEN_SECRET_KEY=getenv('JWT_ACCESS_TOKEN_SECRET_KEY'),
    REFRESH_TOKEN_SECRET_KEY=getenv('JWT_REFRESH_TOKEN_SECRET_KEY')
)
