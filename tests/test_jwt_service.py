from datetime import (
    datetime,
    timedelta
)

import pytest
from jose import jwt

from app.core.config import jwt_config
from app.db.models import User
from app.schemas.jwt import (
    JWTMeta,
    JWTUser
)
from app.services.jwt import UserJWTService
from app.services.jwt.types import (
    TokenPayloadMetaClaims,
    TokenDataForEncoding,
    Token,
    Tokens
)


class TestUserJWTService:
    TEST_META_CLAIMS = TokenPayloadMetaClaims(timedelta(minutes=1), 'subject')
    TEST_TOKEN_SECRET = 'secret'

    @pytest.fixture(name='user')
    def fixture_user(self) -> User:
        return User(email='example@gmail.com', is_superuser=False)

    @pytest.fixture(name='service')
    def fixture_service(self, user: User) -> UserJWTService:
        return UserJWTService(user)

    def test_jwt_user(self, service: UserJWTService):
        assert JWTUser.from_orm(service.user) == service.jwt_user

    def test_generate_tokens(self, service: UserJWTService):
        assert isinstance(service.generate_tokens(), Tokens)

    def test_generate_token(self, service: UserJWTService):
        test_payload = service._prepare_payload(self.TEST_META_CLAIMS)
        manual_token = Token(
            jwt.encode(test_payload, self.TEST_TOKEN_SECRET, jwt_config.ALGORITHM), test_payload['exp']
        )
        service_token = service._generate_token(TokenDataForEncoding(self.TEST_META_CLAIMS, self.TEST_TOKEN_SECRET))
        assert manual_token == service_token

    def test_prepare_payload(self, service: UserJWTService):
        test_payload = service._make_user_payload() | service._make_meta_payload(self.TEST_META_CLAIMS)
        assert test_payload == service._prepare_payload(self.TEST_META_CLAIMS)

    def test_make_user_payload(self, service: UserJWTService):
        assert service.jwt_user.dict() == service._make_user_payload()

    def test_make_meta_payload(self, service: UserJWTService):
        assert JWTMeta.__fields__.keys() == service._make_meta_payload(self.TEST_META_CLAIMS).keys()

    def test_compute_expire(self):
        delta = timedelta(minutes=5)
        assert UserJWTService._compute_expire(delta) == datetime.utcnow() + delta
