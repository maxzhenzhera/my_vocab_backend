import bcrypt
from passlib.context import CryptContext

from .base import BaseUserService
from ..db.models import User


__all__ = ['UserPasswordService']


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserPasswordService(BaseUserService):
    def change_password(self, password: str) -> User:
        self.user.password_salt = self._generate_salt()
        self.user.hashed_password = self._get_password_hash(self._combine_password_with_salt(password=password))
        return self.user

    def verify_password(self, password: str) -> bool:
        return self._verify_password(self._combine_password_with_salt(password=password), self.user.hashed_password)

    def _combine_password_with_salt(self, password: str) -> str:
        return self.user.password_salt + password

    @staticmethod
    def _generate_salt() -> str:
        return bcrypt.gensalt().decode()

    @staticmethod
    def _get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
