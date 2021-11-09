from datetime import datetime

from pydantic import BaseModel


__all__ = ['JWTMeta']


class JWTMeta(BaseModel):
    exp: datetime
    sub: str        # jwt subject must be <str> type
