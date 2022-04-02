from .db import DBSettings
from .jwt import JWTSettings
from .oauth import OAuthSettings
from .password import PasswordSettings
from .tokens import TokensSettings


__all__ = [
    'DBSettings',
    'JWTSettings',
    'OAuthSettings',
    'PasswordSettings',
    'TokensSettings'
]
