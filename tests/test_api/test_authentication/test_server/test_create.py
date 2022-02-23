from typing import (
    Any,
    ClassVar
)

import pytest
from httpx import AsyncClient
from starlette.datastructures import URLPath

from .base import BaseTestUserServerCreationRouteCase
from ...dataclasses_ import MetaUser
from ...mixins.response_and_client import ResponseAndClient


pytestmark = pytest.mark.asyncio


class CreateRouteNameMixin:
    route_name: ClassVar[str] = 'auth:create'


class TestCreateRouteSingleCase(
    CreateRouteNameMixin,
    BaseTestUserServerCreationRouteCase
):
    @pytest.fixture(name='created_user_email')
    def fixture_created_user_email(self, meta_user_1: MetaUser) -> str:
        return meta_user_1.email

    @pytest.fixture(name='success_route_body')
    def fixture_success_route_body(self, meta_user_1: MetaUser) -> dict[str, Any]:
        return meta_user_1.in_create.dict()

    @pytest.fixture(name='response_and_client_on_success')
    async def fixture_response_and_client_on_success(
            self,
            route_url: URLPath,
            success_route_body: dict[str, Any],
            client: AsyncClient
    ) -> ResponseAndClient:
        return (
            await client.post(
                url=route_url,
                json=success_route_body
            ),
            client
        )
