from os import environ

from fastapi_mail import ConnectionConfig as MailConnectionSettings

from .constants.jwt import JWT_ALGORITHM
from .constants.oauth import (
    GOOGLE_OAUTH_CLIENT_KWARGS,
    GOOGLE_OAUTH_NAME,
    GOOGLE_OAUTH_SERVER_METADATA_URL
)
from .constants.tokens import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE
)
from .dataclasses_.app import AppSettings
from .dataclasses_.components import (
    DBSettings,
    JWTSettings,
    OAuthSettings,
    PasswordSettings,
    TokenSettings
)
from .dataclasses_.components.oauth import OAuthProviderSettings
from .dataclasses_.libs import (
    FastAPISettings,
    UvicornSettings
)
from .dataclasses_.middlewares import (
    CORSSettings,
    SessionSettings
)
from .environments import AppEnvironmentType
from .paths import (
    EMAIL_TEMPLATES_DIR,
    LOGGING_CONFIG_PATH
)
from ...utils.casts import (
    to_bool,
    to_list
)


__all__ = ['build_app_settings']


def build_app_settings(env_type: AppEnvironmentType) -> AppSettings:
    return AppSettings(
        # Environment
        # -------------------------------------------
        env_type=env_type,
        # Libs [server setup]
        # -------------------------------------------
        fast_api=FastAPISettings(
            title=environ['APP_TITLE'],
            version=environ['APP_VERSION'],
            docs_url=environ.get('APP_DOCS_URL') or '/docs',
            redoc_url=environ.get('APP_REDOC_URL') or '/redoc'
        ),
        uvicorn=UvicornSettings(
            host=environ['APP_HOST'],
            port=int(environ['APP_PORT']),
            reload=to_bool(environ['APP_RELOAD']),
            logging_config_path=(
                environ.get('LOGGING_CONFIG_PATH') or str(LOGGING_CONFIG_PATH)
            )
        ),
        # Middlewares
        # -------------------------------------------
        cors=CORSSettings(
            origins=to_list(environ['CORS_ORIGINS'], str),
            methods=to_list(environ['CORS_METHODS'], str),
            headers=to_list(environ['CORS_HEADERS'], str)
        ),
        session=SessionSettings(
            secret=environ['SESSION_SECRET']
        ),
        # Components
        # -------------------------------------------
        mail=MailConnectionSettings(
            MAIL_USERNAME=environ['MAIL_USERNAME'],
            MAIL_PASSWORD=environ['MAIL_PASSWORD'],
            MAIL_SERVER=environ['MAIL_SERVER'],
            MAIL_PORT=int(environ['MAIL_PORT']),
            MAIL_FROM=environ['MAIL_FROM'],
            MAIL_FROM_NAME=environ['MAIL_FROM_NAME'],
            MAIL_TLS=to_bool(environ['MAIL_TLS']),
            MAIL_SSL=to_bool(environ['MAIL_SSL']),
            TEMPLATE_FOLDER=EMAIL_TEMPLATES_DIR
        ),
        db=DBSettings(
            uri=environ['DB_URI']
        ),
        jwt=JWTSettings(
            algorithm=JWT_ALGORITHM,
            secret=environ['JWT_SECRET'],
        ),
        oauth=OAuthSettings(
            google=OAuthProviderSettings(
                name=GOOGLE_OAUTH_NAME,
                server_metadata_url=GOOGLE_OAUTH_SERVER_METADATA_URL,
                client_kwargs=GOOGLE_OAUTH_CLIENT_KWARGS,
                client_id=environ['GOOGLE_CLIENT_ID'],
                client_secret=environ['GOOGLE_CLIENT_SECRET']
            )
        ),
        password=PasswordSettings(
            pepper=environ['PASSWORD_PEPPER']
        ),
        access_token=TokenSettings(
            type=ACCESS_TOKEN_TYPE,
            expire_in_seconds=int(environ['ACCESS_TOKEN_EXPIRE_IN_SECONDS'])
        ),
        refresh_token=TokenSettings(
            type=REFRESH_TOKEN_TYPE,
            expire_in_seconds=int(environ['REFRESH_TOKEN_EXPIRE_IN_SECONDS'])
        )
    )
