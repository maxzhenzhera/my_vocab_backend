from os import getenv

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig as MailConnectionConfig
from starlette.config import Config as StarletteConfig

from .dataclasses_ import (
    ServerConfig,
    UvicornConfig,
    DBConfig,
    JWTConfig,
    RefreshSessionConfig
)
from .paths import (
    EMAIL_TEMPLATES_DIR,
    LOGGING_CONFIG_PATH
)
from ..utils.casts import to_bool


__all__ = [
    'CORS_ORIGINS',
    'SESSION_MIDDLEWARE_SECRET_KEY',
    'server_config',
    'uvicorn_config',
    'sqlalchemy_connection_string',
    'mail_connection_config',
    'jwt_config',
    'refresh_session_config',
    'oauth_config'
]


load_dotenv()


CORS_ORIGINS = [origin for origin in getenv('CORS_ORIGINS').split(',')]
SESSION_MIDDLEWARE_SECRET_KEY = getenv('SESSION_MIDDLEWARE_SECRET_KEY')


server_config = ServerConfig(
    HOST=getenv('SERVER_HOST'),
    PORT=int(getenv('SERVER_PORT')),
    API_PREFIX=getenv('API_PREFIX', '/api')
)
uvicorn_config = UvicornConfig(
    SERVER_CONFIG=server_config,
    LOGGING_CONFIG_PATH=LOGGING_CONFIG_PATH,
    RELOAD=to_bool(getenv('UVICORN_RELOAD'))
)
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
    MAIL_FROM=getenv('MAIL_FROM'),      # noqa pydantic email validation
    MAIL_FROM_NAME=getenv('MAIL_FROM_NAME'),
    MAIL_TLS=to_bool(getenv('MAIL_TLS')),
    MAIL_SSL=to_bool(getenv('MAIL_SSL')),
    TEMPLATE_FOLDER=EMAIL_TEMPLATES_DIR
)
jwt_config = JWTConfig(
    ACCESS_TOKEN_SECRET_KEY=getenv('JWT_ACCESS_TOKEN_SECRET_KEY')
)
refresh_session_config = RefreshSessionConfig()
oauth_config = StarletteConfig(
    environ={
        'GOOGLE_CLIENT_ID': getenv('GOOGLE_CLIENT_ID'),
        'GOOGLE_CLIENT_SECRET': getenv('GOOGLE_CLIENT_SECRET')
    }
)
