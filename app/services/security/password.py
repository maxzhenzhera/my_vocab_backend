import secrets
import string

import bcrypt

from .context import pwd_context
from ..base import BaseUserService
from ...db.models import User


__all__ = ['UserPasswordService']


DEFAULT_RANDOM_PASSWORD_LENGTH = 20
DEFAULT_RANDOM_PASSWORD_ALPHABET = string.ascii_letters + string.digits


class UserPasswordService(BaseUserService):
    @staticmethod
    def generate_random_password(
            length: int = DEFAULT_RANDOM_PASSWORD_LENGTH,
            alphabet: str = DEFAULT_RANDOM_PASSWORD_ALPHABET
    ) -> str:
        return ''.join([secrets.choice(alphabet) for _ in range(length)])

    def change_password(self, password: str) -> User:
        self.user.password_salt = self._generate_salt()
        self.user.hashed_password = self._hash_password(
            self._combine_password_with_salt(password)
        )
        return self.user

    def verify_password(self, password: str) -> bool:
        return self._verify_password(
            self._combine_password_with_salt(password),
            self.user.hashed_password
        )

    def _combine_password_with_salt(self, password: str) -> str:
        return self.user.password_salt + password

    @staticmethod
    def _generate_salt() -> str:
        return bcrypt.gensalt().decode()

    @staticmethod
    def _hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
