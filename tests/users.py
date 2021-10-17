from dataclasses import dataclass

from app.schemas.user import (
    UserInCreate,
    UserInLogin
)


__all__ = [
    'TestUser',
    'test_user_1',
    'test_user_2'
]


@dataclass
class TestUser:
    email: str
    password: str

    @property
    def in_create(self) -> UserInCreate:
        return UserInCreate(email=self.email, password=self.password)       # noqa pydantic email validation

    @property
    def in_login(self) -> UserInLogin:
        return UserInLogin(email=self.email, password=self.password)        # noqa pydantic email validation


test_user_1 = TestUser('example1@gmail.com', 'password')
test_user_2 = TestUser('example2@gmail.com', 'password')
