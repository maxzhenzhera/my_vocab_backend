from datetime import (
    datetime,
    timedelta
)

import pytest
from jose.jwt import ALGORITHMS
from pytest_mock import MockerFixture

from app.core.settings.dataclasses_.components import (
    JWTSettings,
    TokenSettings
)
from app.db.models import User
from app.services.jwt import JWTService
from app.services.jwt.dataclasses_ import JWTUser
from app.services.jwt.service import ClaimsFromToken
from ..utils.datetime_ import assert_datetime


class TestJWTService:
    @property
    def computational_interference(self) -> timedelta:
        """ On token encoding microseconds are ignored. """
        return timedelta(seconds=5)

    @pytest.fixture(name='jwt_settings')
    def fixture_jwt_settings(self) -> JWTSettings:
        return JWTSettings(
            algorithm=ALGORITHMS.HS256,
            secret='fake-jwt-secret'
        )

    @pytest.fixture(name='token_settings')
    def fixture_token_settings(self) -> TokenSettings:
        return TokenSettings(
            type='Test',
            expire_in_seconds=600
        )

    @pytest.fixture(name='service')
    def fixture_service(
            self,
            jwt_settings: JWTSettings,
            token_settings: TokenSettings
    ) -> JWTService:
        return JWTService(
            jwt_settings=jwt_settings,
            token_settings=token_settings
        )

    @pytest.fixture(name='user')
    def fixture_user(self) -> User:
        return User(
            id=1,
            email='user@gmail.com',
            is_email_confirmed=True,
            is_superuser=False
        )

    @pytest.fixture(name='token')
    def fixture_token(
            self,
            service: JWTService,
            user: User
    ) -> str:
        return service.generate(user)

    @pytest.fixture(name='verified_token_claims')
    def fixture_verified_token_claims(
            self,
            service: JWTService,
            token: str
    ) -> ClaimsFromToken:
        return service._verify(token)

    @pytest.fixture(name='verified_token_user')
    def fixture_verified_token_user(
            self,
            service: JWTService,
            token: str
    ) -> JWTUser:
        return service.verify(token)

    def test_secret_functions_called_on_token_generating(
            self,
            mocker: MockerFixture,
            service: JWTService,
            user: User
    ):
        secret_function_mock = mocker.patch('jose.jwt.encode')

        service.generate(user)

        secret_function_mock.assert_called_once()

    def test_secret_functions_called_on_token_verifying(
            self,
            mocker: MockerFixture,
            service: JWTService,
            user: User,
            token: str
    ):
        secret_function_mock = mocker.patch('jose.jwt.decode')

        service._verify(token)

        secret_function_mock.assert_called_once()

    def test_token_generating_called_with_needed_claims(
            self,
            mocker: MockerFixture,
            service: JWTService,
            user: User
    ):
        secret_function_mock = mocker.patch('jose.jwt.encode')

        service.generate(user)

        claims = secret_function_mock.call_args.kwargs['claims']
        assert 'sub' in claims
        assert 'exp' in claims
        assert 'email' in claims

    def test_token_sub_claim(
            self,
            user: User,
            verified_token_claims: ClaimsFromToken
    ):
        assert verified_token_claims['sub'] == str(user.id)

    def test_token_exp_claim(
            self,
            token_settings: TokenSettings,
            verified_token_claims: ClaimsFromToken
    ):
        exp: int = verified_token_claims['exp']

        expected = datetime.utcnow() + token_settings.expire_timedelta
        actual = datetime.utcfromtimestamp(exp)

        assert_datetime(
            expected=expected,
            actual=actual,
            delta=self.computational_interference
        )

    def test_token_user_claims(
            self,
            user: User,
            verified_token_user: JWTUser
    ):
        assert verified_token_user.email == user.email
