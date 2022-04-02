from dataclasses import dataclass


__all__ = ['JWTSettings']


@dataclass
class JWTSettings:
    algorithm: str
    secret: str
