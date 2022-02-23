from typing import ClassVar

import pytest
from httpx import (
    AsyncClient,
    Response
)
from starlette.datastructures import URLPath
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST
)

from app.services.authentication.authenticator.cookie import REFRESH_TOKEN_COOKIE_KEY
from .base import BaseTestTerminatingRefreshSessionRouteCase
from ...base import BaseTestRoute
from ...fakers import fake_refresh_token
from ...mixins.response_and_client import ResponseAndClient


pytestmark = pytest.mark.asyncio


class LogoutRouteNameMixin:
    route_name: ClassVar[str] = 'auth:logout'


class TestLogoutRouteSingleCase(
    LogoutRouteNameMixin,
    BaseTestTerminatingRefreshSessionRouteCase
):
    @pytest.fixture(name='refresh_token_before_request')
    async def fixture_refresh_token_before_request(
            self,
            client_1: AsyncClient
    ):
        return client_1.cookies[REFRESH_TOKEN_COOKIE_KEY]

    @pytest.fixture(name='response_and_client_on_success')
    async def fixture_response_and_client_on_success(
            self,
            route_url: URLPath,
            client_1: AsyncClient
    ) -> ResponseAndClient:
        return (
            await client_1.get(
                url=route_url
            ),
            client_1
        )

    def test_response(self, success_response: Response):
        assert success_response.status_code == HTTP_200_OK
        assert success_response.json() is None


class TestCommonErrorsOfLogoutRoute(
    LogoutRouteNameMixin,
    BaseTestRoute
):
    async def test_return_401_error_on_passing_credentials_of_nonexistent_user(
            self,
            route_url: URLPath,
            client_1: AsyncClient
    ):
        """
        On logout has been passed false refresh token cookie.

        Must return 400 Bad Request.
        """

        bad_response = await client_1.get(
            url=route_url,
            cookies={REFRESH_TOKEN_COOKIE_KEY: fake_refresh_token()}
        )

        assert bad_response.status_code == HTTP_400_BAD_REQUEST
