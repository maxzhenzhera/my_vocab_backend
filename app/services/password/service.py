import secrets
import string
from dataclasses import dataclass
from typing import cast

import bcrypt

from .context import pwd_context
from ...core.settings.dataclasses_.components import PasswordSettings
from ...db.models import User


__all__ = ['PasswordService']


DEFAULT_RANDOM_PASSWORD_LENGTH = 20
DEFAULT_RANDOM_PASSWORD_ALPHABET = string.ascii_letters + string.digits


@dataclass
class PasswordService:
    settings: PasswordSettings
    user: User

    @property
    def pepper(self) -> str:
        return self.settings.pepper

    @staticmethod
    def generate_random_password(
            length: int = DEFAULT_RANDOM_PASSWORD_LENGTH,
            alphabet: str = DEFAULT_RANDOM_PASSWORD_ALPHABET
    ) -> str:
        return ''.join([secrets.choice(alphabet) for _ in range(length)])

    def set_password(self, password: str) -> None:
        self.user.salt = self._generate_salt()
        self.user.hashed_password = self._hash_password(
            self._pepper_salt_password(password)
        )

    def verify_password(self, password: str) -> bool:
        return self._verify_password(
            self._pepper_salt_password(password),
            self.user.hashed_password
        )

    def _pepper_salt_password(self, password: str) -> str:
        return self.pepper + self.user.salt + password

    @staticmethod
    def _generate_salt() -> str:
        return bcrypt.gensalt().decode()

    @staticmethod
    def _hash_password(password: str) -> str:
        return cast(str, pwd_context.hash(password))

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        return cast(bool, pwd_context.verify(plain_password, hashed_password))
