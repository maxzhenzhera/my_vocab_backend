from dataclasses import (
    dataclass,
    field
)
from datetime import timedelta
from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig as MailConnectionConfig
from jose import jwt

from ..utils.casts import to_bool


__all__ = [
    'server_config',
    'uvicorn_config',
    'sqlalchemy_connection_string',
    'mail_connection_config',
    'jwt_config'
]


load_dotenv()


APP_DIR = Path(__file__).parent.parent
BASE_DIR = APP_DIR.parent
LOGGING_CONFIG_PATH = APP_DIR / 'utils' / 'logging_' / 'logging_config.yaml'
EMAIL_TEMPLATES_DIR = APP_DIR / 'email_templates'


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
    ACCESS_TOKEN_EXPIRE_TIMEDELTA: timedelta = field(default=timedelta(minutes=30), init=False)
    REFRESH_TOKEN_EXPIRE_TIMEDELTA: timedelta = field(default=timedelta(weeks=1), init=False)
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
mail_connection_config = MailConnectionConfig(
    MAIL_USERNAME=getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=getenv('MAIL_PASSWORD'),
    MAIL_SERVER=getenv('MAIL_SERVER'),
    MAIL_PORT=int(getenv('MAIL_PORT')),
    MAIL_FROM=getenv('MAIL_FROM'),      # noqa
    MAIL_FROM_NAME=getenv('MAIL_FROM_NAME'),
    MAIL_TLS=to_bool(getenv('MAIL_TLS')),
    MAIL_SSL=to_bool(getenv('MAIL_SSL')),
    TEMPLATE_FOLDER=EMAIL_TEMPLATES_DIR
)
jwt_config = JWTConfig(
    ACCESS_TOKEN_SECRET_KEY=getenv('JWT_ACCESS_TOKEN_SECRET_KEY'),
    REFRESH_TOKEN_SECRET_KEY=getenv('JWT_REFRESH_TOKEN_SECRET_KEY')
)
