import secrets
import string
from dataclasses import dataclass
from typing import cast

from .context import pwd_context
from ...db.models import User


__all__ = ['PasswordService']


DEFAULT_RANDOM_PASSWORD_LENGTH = 20
DEFAULT_RANDOM_PASSWORD_ALPHABET = string.ascii_letters + string.digits


@dataclass
class PasswordService:
    user: User

    @staticmethod
    def generate_random_password(
            length: int = DEFAULT_RANDOM_PASSWORD_LENGTH,
            alphabet: str = DEFAULT_RANDOM_PASSWORD_ALPHABET
    ) -> str:
        return ''.join([secrets.choice(alphabet) for _ in range(length)])

    def set(self, password: str) -> None:
        self.user.hashed_password = self._hash(password)

    def verify(self, password: str) -> bool:
        return self._verify(password, self.user.hashed_password)

    @staticmethod
    def _hash(password: str) -> str:
        return cast(str, pwd_context.hash(password))

    @staticmethod
    def _verify(plain_password: str, hashed_password: str) -> bool:
        return cast(bool, pwd_context.verify(plain_password, hashed_password))
