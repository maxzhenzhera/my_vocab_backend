from abc import (
    ABC,
    abstractmethod
)
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from app.services.authentication.oauth.dataclasses_ import OAuthUser


__all__ = [
    'RawOAuthMockMixin',
    'OAuthMockMixin'
]


class RawOAuthMockMixin:
    @pytest.fixture(name='raw_mock_get_oauth_user')
    async def fixture_raw_mock_get_oauth_user(
            self,
            mocker: MockerFixture,
    ) -> MagicMock:
        get_oauth_user_mock = mocker.patch(
            'app.services.authentication'
            '.oauth.base.authorizer.BaseAuthorizer.get_oauth_user'
        )
        return get_oauth_user_mock


class OAuthMockMixin(RawOAuthMockMixin, ABC):
    @pytest.fixture(name='oauth_user')
    @abstractmethod
    def fixture_oauth_user(self) -> OAuthUser:
        """
        The OAuth user that interact in OAuth routes.

        In all OAuth routes test cases
        extracting of OAuth user is mocked.
        Return value of this mock will be this property.
        """

    @pytest.fixture(name='mock_get_oauth_user')
    async def fixture_mock_get_oauth_user(
            self,
            raw_mock_get_oauth_user: MagicMock,
            oauth_user: OAuthUser
    ) -> MagicMock:
        raw_mock_get_oauth_user.return_value = oauth_user
        return raw_mock_get_oauth_user
