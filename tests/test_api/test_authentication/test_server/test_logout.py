from typing import ClassVar

import pytest
from httpx import (
    AsyncClient,
    Response
)
from starlette.datastructures import URLPath
from starlette.status import HTTP_200_OK

from app.services.authentication.authenticator.cookie import REFRESH_TOKEN_COOKIE_KEY
# from ..base import BaseTestTerminatingRefreshSessionRoute
from ....mixins.response_and_client import ResponseAndClient
from ....base import BaseTestRoute

pytestmark = pytest.mark.asyncio


class TestLogoutRoute(BaseTestRoute):
    route_name: ClassVar[str] = 'auth:logout'

    # @pytest.fixture(name='old_refresh_token')
    # @abstractmethod
    # async def fixture_old_refresh_token(self, *args, **kwargs) -> str:
    #     """
    #     Abstract fixture that must return the refresh token from the authenticated user cookie
    #     before that client execute logout/refresh (terminating refresh session) route.
    #
    #         .. code-block:: python
    #
    #             return authenticated_test_client.cookies[REFRESH_TOKEN_COOKIE_KEY]
    #     """
    #
    # async def test_deleting_refresh_session_from_db(        # noqa Method may be 'static'
    #         self,
    #         old_refresh_token: str,
    #         response: Response,
    #         test_refresh_sessions_repository: RefreshSessionsRepository
    # ):
    #     """
    #     The order of the used fixtures is important.
    #     If put
    #         < old_refresh_token >
    #     after
    #         < response >
    #     than it would try to get the cookie from the changed (by route execution) user.
    #     """
    #
    #     with pytest.raises(EntityDoesNotExistError):
    #         await test_refresh_sessions_repository.fetch_by_refresh_token(old_refresh_token)

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

    @pytest.fixture(name='old_refresh_token')
    def fixture_old_refresh_token(self, test_client_user_1: AsyncClient) -> str:
        return test_client_user_1.cookies[REFRESH_TOKEN_COOKIE_KEY]

    def test_response(self, success_response: Response):
        assert success_response.status_code == HTTP_200_OK
        assert success_response.json() is None

    def test_deleting_refresh_token_cookie(self, client: AsyncClient):
        assert REFRESH_TOKEN_COOKIE_KEY not in client.cookies
