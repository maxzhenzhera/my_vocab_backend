from dataclasses import dataclass
from datetime import datetime


__all__ = ['JWTMeta']


@dataclass
class JWTMeta:
    exp: datetime
    sub: str
