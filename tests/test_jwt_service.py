from datetime import (
    datetime,
    timedelta
)
import pytest

from app.services.jwt import UserJWTService
from app.db.models import User


class TestUserJWTService:
    @pytest.fixture(name='user')
    def fixture_user(self) -> User:
        return User(email='example@gmail.com', is_superuser=False)

    @pytest.fixture(name='service')
    def fixture_service(self, user: User) -> UserJWTService:
        return UserJWTService(user)

    def test_compute_expire(self):
        delta = timedelta(minutes=5)
        assert UserJWTService._compute_expire(delta) == datetime.utcnow() + delta
