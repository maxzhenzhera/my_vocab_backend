from dataclasses import dataclass


__all__ = ['OAuthUserCredentials']


@dataclass
class OAuthUserCredentials:
    email: str
    password: str
