from abc import (
    ABC,
    abstractmethod
)
from typing import Any

import pytest
from httpx import AsyncClient
from starlette.datastructures import URLPath
from starlette.status import HTTP_400_BAD_REQUEST

from app.db.models import User
from ...base import BaseTestUserCreationRouteCase


__all__ = ['BaseTestUserServerCreationRouteCase']


class BaseTestUserServerCreationRouteCase(BaseTestUserCreationRouteCase, ABC):
    @pytest.fixture(name='success_route_body')
    @abstractmethod
    def fixture_success_route_body(self) -> str:
        """ Return success route body (JSON). """

    async def test_return_400_error_on_passing_already_used_credentials(
            self,
            route_url: URLPath,
            success_route_body: dict[str, Any],
            success_client: AsyncClient
    ):
        bad_response = await success_client.post(
            url=route_url,
            json=success_route_body
        )

        assert bad_response.status_code == HTTP_400_BAD_REQUEST

    def _test_created_user_claims(self, user: User):
        assert not user.is_email_confirmed
        assert user.email_confirmed_at is None
