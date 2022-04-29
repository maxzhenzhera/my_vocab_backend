from typing import ClassVar

from fastapi_mail.config import ConnectionConfig as MailSettings
from jose.jwt import ALGORITHMS
from pydantic import (
    BaseSettings,
    Field,
    PostgresDsn,
    SecretStr
)

from ..dataclasses_.components import (
    DBSettings,
    JWTSettings,
    OAuthSettings,
    TokensSettings
)
from ..dataclasses_.components.oauth import OAuthProviderSettings
from ..dataclasses_.components.tokens import TokenSettings
from ..dataclasses_.middlewares import (
    CORSSettings,
    SessionSettings
)
from ..dataclasses_.server import (
    FastAPISettings,
    SocketSettings
)
from ..environment import AppEnvType
from ..paths import EMAIL_TEMPLATES_DIR


__all__ = ['AppSettings']


class AppSettings(BaseSettings):
    project_name: ClassVar[str] = 'My Vocab Backend'
    env_type: AppEnvType

    socket_host: str = Field('127.0.0.1', env='APP_HOST')
    socket_port: int = Field(8000, env='APP_PORT')

    fastapi_title: str | None = Field(None, env='APP_TITLE')
    fastapi_version: str = Field('0.1.0', env='APP_VERSION')
    fastapi_docs_url: str = Field('/docs', env='APP_DOCS_URL')
    fastapi_redoc_url: str = Field('/redoc', env='APP_REDOC_URL')

    cors_origins: list[str] = Field(..., env='CORS_ORIGINS')
    cors_methods: list[str] = Field(..., env='CORS_METHODS')
    cors_headers: list[str] = Field(..., env='CORS_HEADERS')

    session_secret: SecretStr = Field(..., env='SESSION_SECRET')

    db_dialect: ClassVar[str] = 'postgresql'
    db_driver: ClassVar[str] = 'asyncpg'
    db_uri: PostgresDsn = Field(..., env='DB_URI')

    jwt_algorithm: ClassVar[str] = ALGORITHMS.HS256
    jwt_secret: SecretStr = Field(..., env='JWT_SECRET')

    mail_username: str = Field(..., env='MAIL_USERNAME')
    mail_password: SecretStr = Field(..., env='MAIL_PASSWORD')
    mail_server: str = Field(..., env='MAIL_SERVER')
    mail_port: int = Field(..., env='MAIL_PORT')
    mail_tls: bool = Field(True, env='MAIL_TLS')
    mail_ssl: bool = Field(False, env='MAIL_SSL')
    mail_from: str = Field(..., env='MAIL_FROM')
    mail_from_name: str = Field(..., env='MAIL_FROM_NAME')
    mail_suppress_send: bool = Field(False, env='MAIL_SUPPRESS_SEND')

    oauth_google_name: ClassVar[str] = 'google'
    oauth_google_server_metadata_url: ClassVar[str] = (
        'https://accounts.google.com/.well-known/openid-configuration'
    )
    oauth_google_client_kwargs: ClassVar[dict[str, str]] = {
        'scope': 'openid email profile'
    }
    oauth_google_client_id: SecretStr = Field(..., env='GOOGLE_CLIENT_ID')
    oauth_google_client_secret: SecretStr = Field(..., env='GOOGLE_CLIENT_SECRET')

    access_token_type: ClassVar[str] = 'Bearer'
    access_token_expire_in_seconds: int = Field(
        ...,
        env='ACCESS_TOKEN_EXPIRE_IN_SECONDS'
    )

    refresh_token_type: ClassVar[str] = 'Bearer'
    refresh_token_expire_in_seconds: int = Field(
        ...,
        env='ACCESS_TOKEN_EXPIRE_IN_SECONDS'
    )

    @property
    def alternative_app_title(self) -> str:
        return f'{self.project_name} {self.env_type.value.capitalize()}'

    @property
    def socket(self) -> SocketSettings:
        return SocketSettings(
            host=self.socket_host,
            port=self.socket_port
        )

    @property
    def fastapi(self) -> FastAPISettings:
        return FastAPISettings(
            title=self.fastapi_title or self.alternative_app_title,
            version=self.fastapi_version,
            docs_url=self.fastapi_docs_url,
            redoc_url=self.fastapi_redoc_url
        )

    @property
    def cors(self) -> CORSSettings:
        return CORSSettings(
            origins=self.cors_origins,
            methods=self.cors_methods,
            headers=self.cors_headers
        )

    @property
    def session(self) -> SessionSettings:
        return SessionSettings(
            secret=self.session_secret.get_secret_value()
        )

    @property
    def db(self) -> DBSettings:
        return DBSettings(
            dialect=self.db_dialect,
            driver=self.db_driver,
            uri=self.db_uri
        )

    @property
    def jwt(self) -> JWTSettings:
        return JWTSettings(
            algorithm=self.jwt_algorithm,
            secret=self.jwt_secret.get_secret_value()
        )

    @property
    def mail(self) -> MailSettings:
        return MailSettings(
            MAIL_USERNAME=self.mail_username,
            MAIL_PASSWORD=self.mail_password.get_secret_value(),
            MAIL_SERVER=self.mail_server,
            MAIL_PORT=self.mail_port,
            MAIL_TLS=self.mail_tls,
            MAIL_SSL=self.mail_ssl,
            MAIL_FROM=self.mail_from,
            MAIL_FROM_NAME=self.mail_from_name,
            SUPPRESS_SEND=self.mail_suppress_send,
            TEMPLATE_FOLDER=EMAIL_TEMPLATES_DIR
        )

    @property
    def oauth(self) -> OAuthSettings:
        return OAuthSettings(
            google=self._oauth_google
        )

    @property
    def _oauth_google(self) -> OAuthProviderSettings:
        return OAuthProviderSettings(
            name=self.oauth_google_name,
            server_metadata_url=self.oauth_google_server_metadata_url,
            client_kwargs=self.oauth_google_client_kwargs,
            client_id=self.oauth_google_client_id.get_secret_value(),
            client_secret=self.oauth_google_client_secret.get_secret_value()
        )

    @property
    def tokens(self) -> TokensSettings:
        return TokensSettings(
            access=self._access_token,
            refresh=self._refresh_token
        )

    @property
    def _access_token(self) -> TokenSettings:
        return TokenSettings(
            type=self.access_token_type,
            expire_in_seconds=self.access_token_expire_in_seconds
        )

    @property
    def _refresh_token(self) -> TokenSettings:
        return TokenSettings(
            type=self.refresh_token_type,
            expire_in_seconds=self.refresh_token_expire_in_seconds
        )
