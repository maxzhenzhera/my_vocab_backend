from abc import (
    ABC,
    abstractmethod
)

import pytest
from httpx import Response

from app.db.errors import EntityDoesNotExistError
from app.db.repositories import RefreshSessionsRepository
from ...base import BaseTestRoute


__all__ = ['BaseTestTerminatingRefreshSessionRoute']


class BaseTestTerminatingRefreshSessionRoute(BaseTestRoute, ABC):
    @pytest.fixture(name='old_refresh_token')
    @abstractmethod
    async def fixture_old_refresh_token(self, *args, **kwargs) -> str:
        """
        Abstract fixture that must return the refresh token from the authenticated user cookie
        before that client execute logout/refresh (terminating refresh session) route.

            .. code-block:: python

                return authenticated_test_client.cookies[REFRESH_TOKEN_COOKIE_KEY]
        """

    async def test_deleting_refresh_session_from_db(        # noqa Method may be 'static'
            self,
            old_refresh_token: str,
            response: Response,
            test_refresh_sessions_repository: RefreshSessionsRepository
    ):
        """
        The order of the used fixtures is important.
        If put
            < old_refresh_token >
        after
            < response >
        than it would try to get the cookie from the changed (by route execution) user.
        """

        with pytest.raises(EntityDoesNotExistError):
            await test_refresh_sessions_repository.fetch_by_refresh_token(old_refresh_token)
