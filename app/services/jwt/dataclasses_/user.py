from dataclasses import dataclass


__all__ = ['JWTUser']


@dataclass
class JWTUser:
    email: str
    is_email_confirmed: bool
    is_superuser: bool
