from datetime import (
    datetime,
    timedelta
)
from time import sleep

import pytest
from jose import jwt

from app.core.config import jwt_config
from app.db.models import User
from app.schemas.jwt import (
    JWTMeta,
    JWTUser
)
from app.services.jwt import UserJWTService
from app.services.jwt.errors import (
    InvalidTokenSignatureError,
    ExpiredTokenSignatureError
)
from app.services.jwt.helpers import decode_token
from app.services.jwt.types import (
    TokenPayloadMetaClaims,
    TokenDataForEncoding,
    TokenDataForDecoding,
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

    def test_tokens_verifying(self, service: UserJWTService):
        tokens = service.generate_tokens()
        assert isinstance(service.verify_access_token(tokens.access_token.token), JWTUser)
        assert isinstance(service.verify_refresh_token(tokens.refresh_token.token), JWTUser)

    def test_decode_token(self, service: UserJWTService):
        common_test_payload = {
            'sub': 'test',
            'data': 'data'
        }
        test_token_expire_in_seconds = 1
        test_payload_for_expire = {
            'exp': service._compute_expire(timedelta(seconds=test_token_expire_in_seconds)),
            **common_test_payload
        }
        test_payload_for_invalid_signature = {
            'exp': service._compute_expire(timedelta(hours=1)),
            **common_test_payload
        }

        test_token_for_expire = jwt.encode(test_payload_for_expire, self.TEST_TOKEN_SECRET, jwt_config.ALGORITHM)
        with pytest.raises(ExpiredTokenSignatureError):
            sleep(test_token_expire_in_seconds + 1)
            decode_token(TokenDataForDecoding(test_token_for_expire, self.TEST_TOKEN_SECRET))

        test_token_for_invalid_signature = jwt.encode(
            test_payload_for_invalid_signature, self.TEST_TOKEN_SECRET, jwt_config.ALGORITHM
        )
        with pytest.raises(InvalidTokenSignatureError):
            test_token_with_injection = test_token_for_invalid_signature + 'injection'
            decode_token(TokenDataForDecoding(test_token_with_injection, self.TEST_TOKEN_SECRET))
        with pytest.raises(InvalidTokenSignatureError):
            test_token_invalid_secret = self.TEST_TOKEN_SECRET + 'invalid'
            decode_token(TokenDataForDecoding(test_token_for_invalid_signature, test_token_invalid_secret))

        normal_result = decode_token(TokenDataForDecoding(test_token_for_invalid_signature, self.TEST_TOKEN_SECRET))
        assert isinstance(normal_result, dict)

    def test_jwt_user(self, service: UserJWTService):
        assert JWTUser.from_orm(service.user) == service.jwt_user

    def test_generate_tokens(self, service: UserJWTService):
        assert isinstance(service.generate_tokens(), Tokens)

    def test_generate_token(self, service: UserJWTService):
        test_payload = service._prepare_payload(self.TEST_META_CLAIMS)
        expires_at = test_payload['exp']
        manual_token = Token(
            jwt.encode(test_payload, self.TEST_TOKEN_SECRET, jwt_config.ALGORITHM), expires_at
        )

        service_token = service._generate_token(TokenDataForEncoding(self.TEST_META_CLAIMS, self.TEST_TOKEN_SECRET))

        assert isinstance(service_token.expires_at, datetime)
        # GitHub Actions time difference on computing
        assert manual_token.token == service_token.token

    def test_prepare_payload(self, service: UserJWTService):
        test_payload = service._make_user_payload() | service._make_meta_payload(self.TEST_META_CLAIMS)
        service_payload = service._prepare_payload(self.TEST_META_CLAIMS)
        # GitHub Actions time difference on computing
        del test_payload['exp']
        del service_payload['exp']
        assert test_payload == service_payload

    def test_make_user_payload(self, service: UserJWTService):
        assert service.jwt_user.dict() == service._make_user_payload()

    def test_make_meta_payload(self, service: UserJWTService):
        assert JWTMeta.__fields__.keys() == service._make_meta_payload(self.TEST_META_CLAIMS).keys()

    def test_compute_expire(self):
        # GitHub Actions time difference on computing
        computational_interference = timedelta(seconds=10)
        test_delta = timedelta(minutes=5)
        service_expire = UserJWTService._compute_expire(test_delta)
        manual_expire = datetime.utcnow() + test_delta
        assert (manual_expire - service_expire) < computational_interference
