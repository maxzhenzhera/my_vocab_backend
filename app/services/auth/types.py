from dataclasses import dataclass

from ..jwt.types import Token
from ...db.models import User


__all__ = ['RefreshSessionData']


@dataclass
class RefreshSessionData:
    user: User
    refresh_token: Token
