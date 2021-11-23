from datetime import (
    datetime,
    timedelta
)

import pytest

from app.core.config import jwt_config
from app.db.models import User
from app.schemas.jwt import JWTUser
from app.services.jwt import UserJWTService


class TestUserJWTService:
    @pytest.fixture(name='user')
    def fixture_user(self) -> User:
        return User(
            id=1,
            email='example@gmail.com',
            is_superuser=False,
            is_email_confirmed=False
        )

    @pytest.fixture(name='service')
    def fixture_service(self, user: User) -> UserJWTService:
        return UserJWTService(user)

    @pytest.fixture(name='access_token')
    def fixture_access_token(self, service: UserJWTService) -> str:
        return service.generate_access_token()

    def test_jwt_user(self, service: UserJWTService):
        assert service.jwt_user == JWTUser.from_orm(service.user)

    def test_verify_access_token(self, access_token: str, service: UserJWTService):
        assert isinstance(service.verify_access_token(access_token), JWTUser)

    def test_generate_access_token(self, service: UserJWTService):
        assert isinstance(service.generate_access_token(), str)

    def test_prepare_payload(self, service: UserJWTService):
        test_payload = service._make_user_payload() | service._make_meta_payload()
        service_payload = service._prepare_payload()

        # GitHub Actions time difference on computing
        computational_interference = timedelta(seconds=10)
        assert test_payload.pop('exp') - service_payload.pop('exp') < computational_interference

        assert test_payload == service_payload

    def test_make_user_payload(self, service: UserJWTService):
        assert service._make_user_payload() == service.jwt_user.dict()

    def test_make_meta_payload(self, service: UserJWTService):
        meta_payload = service._make_meta_payload()

        assert 'exp' in meta_payload
        assert 'sub' in meta_payload

    def test_compute_expire(self):
        # GitHub Actions time difference on computing
        computational_interference = timedelta(seconds=10)
        service_expire = UserJWTService._compute_expire()
        manual_expire = datetime.utcnow() + jwt_config.ACCESS_TOKEN_EXPIRE_TIMEDELTA

        assert (manual_expire - service_expire) < computational_interference
