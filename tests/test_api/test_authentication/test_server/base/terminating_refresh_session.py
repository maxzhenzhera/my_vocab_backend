from abc import (
    ABC,
    abstractmethod
)
from typing import Any

import pytest
from httpx import (
    AsyncClient,
    Response
)

from app.db.repos import RefreshSessionsRepo
from app.services.authentication.authenticator.cookie import REFRESH_TOKEN_COOKIE_KEY
from ....base import BaseTestRouteCase


__all__ = ['BaseTestTerminatingRefreshSessionRouteCase']


class BaseTestTerminatingRefreshSessionRouteCase(BaseTestRouteCase, ABC):
    @pytest.fixture(name='refresh_token_before_request')
    @abstractmethod
    async def fixture_refresh_token_before_request(self, *args: Any):
        """
        Return the refresh token from the authenticated user`s cookie
        before that client execute logout/refresh (terminating refresh session) route.
        """

    def test_deleting_issued_refresh_token_from_cookies(
            self,
            refresh_token_before_request: str,
            success_client: AsyncClient
    ):
        refresh_token_after_request = success_client.cookies.get(
            name=REFRESH_TOKEN_COOKIE_KEY,
            default=''
        )
        assert refresh_token_before_request != refresh_token_after_request

    async def test_deleting_issued_refresh_session_from_db(
            self,
            refresh_token_before_request: str,
            success_response: Response,
            refresh_sessions_repo: RefreshSessionsRepo
    ):
        assert not await refresh_sessions_repo.exists_by_token(
            refresh_token_before_request
        )
