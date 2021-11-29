from typing import ClassVar

import pytest
from httpx import AsyncClient
from starlette.datastructures import URLPath
from starlette.status import HTTP_401_UNAUTHORIZED

from app.main import app
from ...base import BaseTestAuthRoute
from ....base import BaseTestPostRoute
from ....mixins.response_and_client import ResponseAndClient
from .....users import test_user_1


pytestmark = pytest.mark.asyncio


class TestLoginRoute(BaseTestPostRoute, BaseTestAuthRoute):
    url: ClassVar[URLPath] = app.url_path_for('auth:login')
    request_json: ClassVar[dict] = test_user_1.in_login.dict()

    @pytest.fixture(name='response_and_client')
    async def fixture_response_and_client(
            self,
            test_unauthenticated_client_user_1: AsyncClient
    ) -> ResponseAndClient:
        return (
            await test_unauthenticated_client_user_1.post(self.url, json=self.request_json),
            test_unauthenticated_client_user_1
        )

    async def test_return_401_error_on_passing_false_credentials(
            self,
            test_client: AsyncClient
    ):
        """
        On login has been passed the credentials of the nonexistent user.
        Note:
            In the test above used 'test_client_user_1' that means
                'test_user_1' is created (during 'test_client_user_1' initialization).
            Here used simple 'test_client' that means
                no one user does exist under this client.

        Must return 401 Unauthorized.
        """

        response = await test_client.post(self.url, json=self.request_json)

        assert response.status_code == HTTP_401_UNAUTHORIZED
