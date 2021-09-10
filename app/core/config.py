from dataclasses import dataclass, field
from pathlib import Path
from os import getenv

from dotenv import load_dotenv


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
    LOGGING_CONFIG_PATH: str = str(LOGGING_CONFIG_PATH)
    RELOAD: bool = True

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


server_config = ServerConfig(
    getenv('SERVER_HOST'),
    int(getenv('SERVER_PORT')),
    getenv('API_PREFIX', '/api')
)
uvicorn_config = UvicornConfig(server_config).get_config()
sqlalchemy_connection_string = DBConfig(
    getenv('DB_HOST'),
    int(getenv('DB_PORT')),
    getenv('DB_NAME'),
    getenv('DB_USER'),
    getenv('DB_PASSWORD'),
).sqlalchemy_connection_string
