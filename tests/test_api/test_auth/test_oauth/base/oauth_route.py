from abc import (
    ABC,
    abstractmethod
)
from unittest.mock import MagicMock

import pytest
from authlib.integrations.starlette_client import OAuthError
from httpx import AsyncClient
from pytest_mock import MockerFixture
from starlette.status import HTTP_400_BAD_REQUEST

from app.schemas.authentication.oauth import OAuthUser
from ...base import BaseTestAuthRoute


__all__ = ['BaseTestOAuthRoute']


class BaseTestOAuthRoute(BaseTestAuthRoute, ABC):
    @property
    @abstractmethod
    def oauth_user(self) -> OAuthUser:
        """
        The OAuth user that interact in OAuth routes.

        In all OAuth routes test cases
        extracting of OAuth user is mocked.
        Return value of this mock will be this property.

        Abstract *class* attribute:
            oauth_user: ClassVar[OAuthUser] = test_user.service_name_oauth_user
        """

    @pytest.fixture(name='mock_get_oauth_user')
    async def fixture_mock_get_oauth_user(self, mocker: MockerFixture) -> MagicMock:
        get_oauth_user_mock = mocker.patch(
            'app.services.authentication.oauth.base.authorizer.BaseAuthorizer.get_oauth_user'
        )
        get_oauth_user_mock.return_value = self.oauth_user
        return get_oauth_user_mock

    async def test_return_400_error_on_oauth_error(
            self,
            mock_get_oauth_user: MagicMock,
            test_client: AsyncClient
    ):
        mock_get_oauth_user.side_effect = OAuthError

        response = await test_client.get(self.url)

        assert response.status_code == HTTP_400_BAD_REQUEST
