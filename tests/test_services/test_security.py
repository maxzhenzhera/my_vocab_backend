from typing import ClassVar

import pytest
from pytest_mock import MockerFixture

from app.db.models import User
from app.services.security import UserPasswordService


class TestUserPasswordService:
    initial_password: ClassVar[str] = 'old_password'
    new_password: ClassVar[str] = 'new_password'

    @pytest.fixture(name='user')
    def fixture_user(self) -> User:
        return User(email='example@gmail.com')

    @pytest.fixture(name='service')
    def fixture_service(self, user: User) -> UserPasswordService:
        service = UserPasswordService(user)
        service.change_password(self.initial_password)
        return service

    def test_secret_functions_called_on_random_password_generating(
            self,
            mocker: MockerFixture,
            service: UserPasswordService
    ):
        secret_function_mock = mocker.patch('secrets.choice')
        secret_function_mock.return_value = ' '

        length = 10
        service.generate_random_password(length=length)

        assert secret_function_mock.call_count == length

    def test_generate_random_password(self, service: UserPasswordService):
        length = 10
        password = service.generate_random_password(length=length)

        assert len(password) == length

    def test_secret_functions_called_on_password_change(
            self,
            mocker: MockerFixture,
            service: UserPasswordService
    ):
        salt_function_mock = mocker.patch('bcrypt.gensalt')
        hash_function_mock = mocker.patch('passlib.context.CryptContext.hash')

        service.change_password(self.new_password)

        salt_function_mock.assert_called_once()
        hash_function_mock.assert_called_once()

    def test_change_password(self, service: UserPasswordService):
        old_hashed_password = service.user.hashed_password
        old_password_salt = service.user.password_salt

        changed_user = service.change_password(self.new_password)

        new_hashed_password = changed_user.hashed_password
        new_password_salt = changed_user.password_salt

        assert old_hashed_password != new_hashed_password
        assert old_password_salt != new_password_salt

    def test_secret_functions_called_on_password_verifying(
            self,
            mocker: MockerFixture,
            service: UserPasswordService
    ):
        verify_function_mock = mocker.patch('passlib.context.CryptContext.verify')

        service.verify_password(self.initial_password)

        verify_function_mock.assert_called_once()

    def test_verify_password(self, service: UserPasswordService):
        assert service.verify_password(self.initial_password)
        assert not service.verify_password(self.new_password)

    def test_combine_password_with_salt(self, service: UserPasswordService):
        expected = service._combine_password_with_salt(self.new_password)
        actual = service.user.password_salt + self.new_password
        assert actual == expected
