from abc import (
    ABC,
    abstractmethod
)
from unittest.mock import MagicMock

import pytest
from httpx import AsyncClient
from starlette.status import HTTP_401_UNAUTHORIZED

from app.db.repositories import OAuthConnectionsRepo
from .oauth_route import BaseTestOAuthRoute
from ....mixins.response_and_client import ResponseAndClient


__all__ = ['BaseOauthLoginRoute']


class BaseOauthLoginRoute(BaseTestOAuthRoute, ABC):
    @pytest.mark.usefixtures('mock_get_oauth_user')
    @abstractmethod
    async def test_creating_oauth_connection_in_db_on_existed_user_login(
            self,
            test_oauth_connections_repository: OAuthConnectionsRepo,
            *args
    ):
        """
        If
            the existed user that has not linked OAuth connections
        login
            throw OAuth route
        then
            this OAuth connection must be linked to this user.

        So, OAuth connection record
        must be created or updated (if user has other OAuth connections).
        """

    @pytest.fixture(name='response_and_client')
    async def fixture_response_and_client(
            self,
            mock_get_oauth_user: MagicMock,
            test_unauthenticated_client_user_1_with_oauth: AsyncClient
    ) -> ResponseAndClient:
        return (
            await test_unauthenticated_client_user_1_with_oauth.get(self.url),
            test_unauthenticated_client_user_1_with_oauth
        )

    @pytest.mark.usefixtures('mock_get_oauth_user')
    async def test_return_401_error_on_non_existed_user_login(
            self,
            test_client: AsyncClient
    ):
        response = await test_client.get(self.url)

        assert response.status_code == HTTP_401_UNAUTHORIZED
