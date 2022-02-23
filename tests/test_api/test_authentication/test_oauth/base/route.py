from abc import (
    ABC,
    abstractmethod
)
from datetime import timedelta
from unittest.mock import MagicMock

import pytest
from authlib.integrations.starlette_client import OAuthError
from httpx import AsyncClient
from starlette.datastructures import URLPath
from starlette.status import HTTP_400_BAD_REQUEST

from app.db.models import OAuthConnection
from app.db.repos import OAuthConnectionsRepo
from app.services.authentication.oauth.dataclasses_ import OAuthUser
from ..mixins import (
    OAuthMockMixin,
    RawOAuthMockMixin
)
from ...base import BaseTestAuthRouteCase
from ....base import BaseTestRoute
from .....utils.datetime_ import assert_datetime


__all__ = [
    'BaseTestOAuthRouteCase',
    'BaseTestOAuthRouteCaseWhenConnectionCreating',
    'BaseTestCommonErrorsOfOAuthRoute'
]


class BaseTestOAuthRouteCase(
    BaseTestAuthRouteCase,
    OAuthMockMixin,
    ABC
):
    """ Auth route tests combined with mocking OAuth interaction. """


class BaseTestOAuthRouteCaseWhenConnectionCreating(
    BaseTestOAuthRouteCase,
    ABC
):
    """
    OAuth route case when OAuth connection
    have to be created after request.

    When:
        - registration route:
          binds OAuth connection on moment of user creating.
        - login route:
          executed by user that has not bound to OAuth connection
          (has been registered through own auth system or another OAuth).
    """

    @pytest.mark.usefixtures('success_response')
    async def test_creating_oauth_connection_in_db(
            self,
            oauth_user: OAuthUser,
            oauth_connections_repo: OAuthConnectionsRepo
    ):
        oauth_connection = await self._fetch_oauth_connection(
            oauth_user,
            oauth_connections_repo,
        )

        assert_datetime(
            actual=oauth_connection.updated_at,
            delta=timedelta(seconds=5)
        )

    @abstractmethod
    async def _fetch_oauth_connection(
            self,
            oauth_user: OAuthUser,
            repo: OAuthConnectionsRepo,
    ) -> OAuthConnection:
        """
        Has the same logic as:
            app.services.authentication
            .oauth.google.service.GoogleOAuthService._fetch_oauth_connection
        """


class BaseTestCommonErrorsOfOAuthRoute(
    BaseTestRoute,
    RawOAuthMockMixin,
    ABC
):
    @pytest.fixture(name='mock_get_oauth_user')
    def fixture_mock_get_oauth_user(
            self,
            raw_mock_get_oauth_user: MagicMock,
    ) -> MagicMock:
        raw_mock_get_oauth_user.side_effect = OAuthError
        return raw_mock_get_oauth_user

    @pytest.mark.usefixtures('mock_get_oauth_user')
    async def test_return_400_error_on_oauth_error(
            self,
            route_url: URLPath,
            client: AsyncClient
    ):
        bad_response = await client.get(route_url)

        assert bad_response.status_code == HTTP_400_BAD_REQUEST
