from typing import ClassVar

import pytest
from httpx import AsyncClient
from starlette.datastructures import URLPath
from starlette.status import HTTP_401_UNAUTHORIZED

from app.db.repositories import RefreshSessionsRepository
from app.main import app
from app.services.authentication.cookie import REFRESH_TOKEN_COOKIE_KEY
from ..base import BaseTestTerminatingRefreshSessionRoute
from ...base import BaseTestAuthRoute
from ....mixins.response_and_client import ResponseAndClient
from .....helpers.refresh_token import generate_fake_refresh_token


pytestmark = pytest.mark.asyncio


class TestRefreshRoute(BaseTestAuthRoute, BaseTestTerminatingRefreshSessionRoute):
    url: ClassVar[URLPath] = app.url_path_for('auth:refresh')

    @pytest.fixture(name='response_and_client')
    async def fixture_response_and_client(
            self,
            test_client_user_1: AsyncClient
    ) -> ResponseAndClient:
        return await test_client_user_1.get(self.url), test_client_user_1

    @pytest.fixture(name='old_refresh_token')
    def fixture_old_refresh_token(self, test_client_user_1: AsyncClient) -> str:
        return test_client_user_1.cookies[REFRESH_TOKEN_COOKIE_KEY]

    def test_deleting_old_refresh_token_cookie(
            self,
            old_refresh_token: str,
            client: AsyncClient
    ):
        """
        The order of the used fixtures is important.
        If put
            < old_refresh_token >
        after
            < client >
        than it would try to get the cookie from the refreshed user.
        """

        assert client.cookies[REFRESH_TOKEN_COOKIE_KEY] != old_refresh_token

    async def test_return_401_error_on_expired_session(
            self,
            old_refresh_token: str,
            test_client_user_1: AsyncClient,
            test_refresh_sessions_repository: RefreshSessionsRepository
    ):
        """
        On refresh has been passed refresh token which session has been manually expired.

        Must return 401 Unauthorized.
        """

        async with test_refresh_sessions_repository.session.begin():
            await test_refresh_sessions_repository.expire(old_refresh_token)

        response = await test_client_user_1.get(self.url)

        assert response.status_code == HTTP_401_UNAUTHORIZED

    async def test_return_401_error_on_passing_false_refresh_token(
            self,
            test_client_user_1: AsyncClient
    ):
        """
        On refresh has been passed fake refresh token which session does not exist.

        Must return 401 Unauthorized.
        """

        test_client_user_1.cookies[REFRESH_TOKEN_COOKIE_KEY] = generate_fake_refresh_token()
        response = await test_client_user_1.get(self.url)

        assert response.status_code == HTTP_401_UNAUTHORIZED
