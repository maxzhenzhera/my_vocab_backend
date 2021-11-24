from typing import ClassVar

import pytest
from httpx import (
    AsyncClient,
    Response
)
from starlette.datastructures import URLPath
from starlette.status import HTTP_200_OK

from app.main import app
from app.services.authentication.cookie import REFRESH_TOKEN_COOKIE_KEY
from ..base import BaseTestTerminatingRefreshSessionRoute
from ...mixins.response_and_client import ResponseAndClient


pytestmark = pytest.mark.asyncio


class TestLogoutRoute(BaseTestTerminatingRefreshSessionRoute):
    url: ClassVar[URLPath] = app.url_path_for('auth:logout')

    @pytest.fixture(name='response_and_client')
    async def fixture_response_and_client(
            self,
            test_client_user_1: AsyncClient
    ) -> ResponseAndClient:
        return await test_client_user_1.get(self.url), test_client_user_1

    @pytest.fixture(name='old_refresh_token')
    def fixture_old_refresh_token(self, test_client_user_1: AsyncClient) -> str:
        return test_client_user_1.cookies[REFRESH_TOKEN_COOKIE_KEY]

    def test_response(self, response: Response):
        response_json = response.json()

        assert response.status_code == HTTP_200_OK
        assert response_json is None

    def test_deleting_refresh_token_cookie(self, client: AsyncClient):
        assert REFRESH_TOKEN_COOKIE_KEY not in client.cookies
