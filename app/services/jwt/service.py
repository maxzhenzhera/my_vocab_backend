from dataclasses import (
    asdict,
    dataclass
)
from datetime import datetime
from typing import (
    TypeAlias,
    cast
)

from jose import jwt

from .dataclasses_ import (
    JWTMeta,
    JWTUser
)
from ...core.settings.dataclasses_.components import (
    JWTSettings,
    TokenSettings
)
from ...db.models import User
from ...utils.casts import to_dataclass


__all__ = [
    'ClaimsToToken',
    'ClaimsFromToken',
    'JWTService'
]


ClaimsToToken: TypeAlias = dict[str, str | bool | datetime]
# on token encoding `datetime` objects are converting to `int`
ClaimsFromToken: TypeAlias = dict[str, str | bool | int]


@dataclass
class JWTService:
    """
    Implements a base token handler
    to create a particular token handler for the corresponded type.
    """

    jwt_settings: JWTSettings
    token_settings: TokenSettings

    def verify(self, token: str) -> JWTUser:
        return to_dataclass(JWTUser, self._verify(token))

    def _verify(self, token: str) -> ClaimsFromToken:
        return cast(
            ClaimsFromToken,
            jwt.decode(
                token=token,
                key=self.jwt_settings.secret,
                algorithms=self.jwt_settings.algorithm
            )
        )

    def generate(self, user: User) -> str:
        return cast(
            str,
            jwt.encode(
                claims=self._prepare_claims(user),
                key=self.jwt_settings.secret,
                algorithm=self.jwt_settings.algorithm
            )
        )

    def _prepare_claims(self, user: User) -> ClaimsToToken:
        meta_claims = self._form_meta_claims(user)
        user_claims = to_dataclass(JWTUser, user)
        return asdict(meta_claims) | asdict(user_claims)

    def _form_meta_claims(self, user: User) -> JWTMeta:
        return JWTMeta(
            exp=self._compute_expire(),
            sub=str(user.id)
        )

    def _compute_expire(self) -> datetime:
        return datetime.utcnow() + self.token_settings.expire_timedelta
