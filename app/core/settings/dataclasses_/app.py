from dataclasses import dataclass

from fastapi_mail import ConnectionConfig as MailConnectionSettings

from .components import (
    DBSettings,
    JWTSettings,
    OAuthSettings,
    PasswordSettings,
    TokenSettings
)
from .libs import (
    FastAPISettings,
    UvicornSettings
)
from .middlewares import (
    CORSSettings,
    SessionSettings
)
from ..environments import AppEnvironmentType


__all__ = ['AppSettings']


@dataclass(frozen=True)
class AppSettings:
    # Environment
    # -------------------------------------------
    env_type: AppEnvironmentType
    # Libs [server setup]
    # -------------------------------------------
    fast_api: FastAPISettings
    uvicorn: UvicornSettings
    # Middlewares
    # -------------------------------------------
    cors: CORSSettings
    session: SessionSettings
    # Components
    # -------------------------------------------
    mail: MailConnectionSettings
    db: DBSettings
    jwt: JWTSettings
    oauth: OAuthSettings
    password: PasswordSettings
    access_token: TokenSettings
    refresh_token: TokenSettings
