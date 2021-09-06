from dataclasses import dataclass
from pathlib import Path
from os import getenv

from dotenv import load_dotenv


__all__ = [
    'server_config',
    'uvicorn_config'
]


load_dotenv()


APP_DIR = Path(__file__).parent.parent
BASE_DIR = APP_DIR.parent
LOGGING_CONFIG_PATH = APP_DIR / 'utils' / 'logging_' / 'logging_config.yaml'


@dataclass
class ServerConfig:
    HOST: str
    PORT: int


@dataclass
class UvicornConfig:
    SERVER_CONFIG: ServerConfig
    LOGGING_CONFIG_PATH: str
    RELOAD: bool = True

    def get_config(self) -> dict:
        return {
            'host': self.SERVER_CONFIG.HOST,
            'port': self.SERVER_CONFIG.PORT,
            'log_config': str(self.LOGGING_CONFIG_PATH),
            'reload': self.RELOAD
        }


server_config = ServerConfig(
    getenv('SERVER_HOST'),
    int(getenv('SERVER_PORT'))
)
uvicorn_config = UvicornConfig(
    server_config,
    LOGGING_CONFIG_PATH
).get_config()
