from abc import ABC
from unittest.mock import MagicMock

import pytest
from httpx import AsyncClient
from starlette.datastructures import URLPath

from .route import (
    BaseTestOAuthRouteCase,
    BaseTestOAuthRouteCaseWhenConnectionCreating
)
from ....dataclasses_ import MetaUser
from ....mixins.response_and_client import ResponseAndClient


__all__ = [
    'BaseTestOAuthLoginRouteCase',
    'BaseTestOAuthLoginRouteCaseByUserWithOAuth',
    'BaseTestOAuthLoginRouteCaseByUserWithoutOAuth'
]


class BaseTestOAuthLoginRouteCase(
    BaseTestOAuthRouteCase,
    ABC
):
    @pytest.fixture(name='used_meta_user')
    def fixture_used_meta_user(self, meta_user_1: MetaUser) -> MetaUser:
        return meta_user_1


class BaseTestOAuthLoginRouteCaseByUserWithOAuth(
    BaseTestOAuthLoginRouteCase,
    ABC
):
    """ WithOAuth means client with OAuth connection. """
    @pytest.fixture(name='response_and_client_on_success')
    async def fixture_response_and_client_on_success(
            self,
            # apply mocking
            # -----------------------------
            mock_get_oauth_user: MagicMock,
            # -----------------------------
            route_url: URLPath,
            unauthenticated_client_1_with_oauth: AsyncClient
    ) -> ResponseAndClient:
        return (
            await unauthenticated_client_1_with_oauth.get(
                url=route_url
            ),
            unauthenticated_client_1_with_oauth
        )


class BaseTestOAuthLoginRouteCaseByUserWithoutOAuth(
    BaseTestOAuthLoginRouteCase,
    BaseTestOAuthRouteCaseWhenConnectionCreating,
    ABC
):
    """ WithOAuth means client without OAuth connection. """
    @pytest.fixture(name='response_and_client_on_success')
    async def fixture_response_and_client_on_success(
            self,
            # apply mocking
            # -----------------------------
            mock_get_oauth_user: MagicMock,
            # -----------------------------
            route_url: URLPath,
            unauthenticated_client_1: AsyncClient
    ) -> ResponseAndClient:
        return (
            await unauthenticated_client_1.get(
                url=route_url
            ),
            unauthenticated_client_1
        )
