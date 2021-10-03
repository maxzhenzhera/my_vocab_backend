from os import getenv

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig as MailConnectionConfig

from .dataclasses_ import (
    ServerConfig,
    UvicornConfig,
    DBConfig,
    JWTConfig
)
from .paths import EMAIL_TEMPLATES_DIR
from ...utils.casts import to_bool


__all__ = [
    'server_config',
    'uvicorn_config',
    'sqlalchemy_connection_string',
    'mail_connection_config',
    'jwt_config'
]


load_dotenv()


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
    ACCESS_TOKEN_SECRET_KEY=getenv('JWT_ACCESS_TOKEN_SECRET_KEY'),
    REFRESH_TOKEN_SECRET_KEY=getenv('JWT_REFRESH_TOKEN_SECRET_KEY')
)
