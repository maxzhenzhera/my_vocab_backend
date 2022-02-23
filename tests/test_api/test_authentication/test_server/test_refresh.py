from typing import ClassVar

import pytest
from httpx import AsyncClient
from starlette.datastructures import URLPath
from starlette.status import HTTP_401_UNAUTHORIZED

from app.db.repos import RefreshSessionsRepo
from app.services.authentication.authenticator.cookie import REFRESH_TOKEN_COOKIE_KEY
from .base import BaseTestTerminatingRefreshSessionRouteCase
from ..base import BaseTestAuthRouteCase
from ...base import BaseTestRoute
from ...fakers import fake_refresh_token
from ...mixins.response_and_client import ResponseAndClient


pytestmark = pytest.mark.asyncio


class RefreshRouteNameMixin:
    route_name: ClassVar[str] = 'auth:refresh'


class TestRefreshRouteSingleCase(
    RefreshRouteNameMixin,
    BaseTestAuthRouteCase,
    BaseTestTerminatingRefreshSessionRouteCase
):
    @pytest.fixture(name='refresh_token_before_request')
    def fixture_refresh_token_before_request(self, client_1: AsyncClient) -> str:
        return client_1.cookies[REFRESH_TOKEN_COOKIE_KEY]

    @pytest.fixture(name='response_and_client_on_success')
    async def fixture_response_and_client_on_success(
            self,
            route_url: URLPath,
            client_1: AsyncClient
    ) -> ResponseAndClient:
        return (
            await client_1.get(
                url=route_url,
            ),
            client_1
        )


class TestCommonErrorsOfRefreshRoute(
    RefreshRouteNameMixin,
    BaseTestRoute
):
    async def test_return_401_error_on_passing_nonexistent_refresh_token(
            self,
            route_url: URLPath,
            client: AsyncClient
    ):
        """
        On refresh has been passed fake refresh token which session does not exist.

        Must return 401 Unauthorized.
        """

        unauthorized_response = await client.get(
            url=route_url,
            cookies={REFRESH_TOKEN_COOKIE_KEY: fake_refresh_token()}
        )

        assert unauthorized_response.status_code == HTTP_401_UNAUTHORIZED

    async def test_return_401_error_on_expired_session(
            self,
            route_url: URLPath,
            client_1: AsyncClient,
            refresh_sessions_repo: RefreshSessionsRepo
    ):
        """
        On refresh has been passed refresh token
        which session has been manually expired.

        Must return 401 Unauthorized.
        """

        refresh_token = client_1.cookies[REFRESH_TOKEN_COOKIE_KEY]
        async with refresh_sessions_repo.session.begin():
            await refresh_sessions_repo.expire(refresh_token)

        unauthorized_response = await client_1.get(route_url)

        assert unauthorized_response.status_code == HTTP_401_UNAUTHORIZED
