from typing import ClassVar

import pytest
from httpx import AsyncClient
from starlette.datastructures import URLPath

from app.main import app
from ..base import BaseTestUserCreationRoute
from ....mixins.response_and_client import ResponseAndClient
from .....users import test_user_1


pytestmark = pytest.mark.asyncio


class TestCreateRoute(BaseTestUserCreationRoute):
    url: ClassVar[URLPath] = app.url_path_for('auth:create')
    request_json: ClassVar[dict] = test_user_1.in_create.dict()
    created_user_email: ClassVar[str] = test_user_1.email

    @pytest.fixture(name='response_and_client')
    async def fixture_response_and_client(self, test_client: AsyncClient) -> ResponseAndClient:
        return await test_client.post(self.url, json=self.request_json), test_client
