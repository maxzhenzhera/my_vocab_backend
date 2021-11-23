import pytest

from app.db.models import User
from app.services.security import UserPasswordService


class TestUserPasswordService:
    INITIAL_PASSWORD = 'old_password'
    NEW_PASSWORD = 'new_password'

    @pytest.fixture(name='user')
    def fixture_user(self) -> User:
        return User(email='example@gmail.com')

    @pytest.fixture(name='service')
    def fixture_service(self, user: User) -> UserPasswordService:
        service = UserPasswordService(user)
        service.change_password(self.INITIAL_PASSWORD)
        return service

    def test_change_password(self, service: UserPasswordService):
        old_hashed_password = service.user.hashed_password
        old_password_salt = service.user.password_salt

        changed_user = service.change_password(self.NEW_PASSWORD)

        new_hashed_password = changed_user.hashed_password
        new_password_salt = changed_user.password_salt

        assert old_hashed_password != new_hashed_password
        assert old_password_salt != new_password_salt

    def test_verify_password(self, service: UserPasswordService):
        assert service.verify_password(self.INITIAL_PASSWORD)
        assert not service.verify_password(self.NEW_PASSWORD)

    def test_combine_password_with_salt(self, service: UserPasswordService):
        expected = service._combine_password_with_salt(self.NEW_PASSWORD)
        actual = service.user.password_salt + self.NEW_PASSWORD
        assert expected == actual
