from abc import (
    ABC,
    abstractmethod
)
from typing import Any

import pytest
from httpx import Response

from app.db.models import User
from app.db.repos import UsersRepo
from ...base import BaseTestRouteCase


__all__ = ['BaseTestUserCreationRouteCase']


class BaseTestUserCreationRouteCase(BaseTestRouteCase, ABC):
    @pytest.fixture(name='created_user_email')
    @abstractmethod
    def fixture_created_user_email(self) -> str:
        """ The created user email. """

    @abstractmethod
    def test_return_400_error_on_passing_already_used_credentials(self, *args: Any):
        """
        On user creation route has been passed already used credentials.

        Must return 400 Bad Request.
        """

    @abstractmethod
    def _test_created_user_claims(
            self,
            user: User
    ):
        """
        On route execution new user must be created in db.

        User might be created through:
            1. server (own authentication system);
            2. oauth.

        Server user:
            1. is_email_confirmed == False
            2. email_confirmed_at == None

        OAuth User:
            1. is_email_confirmed == True
            2. email_confirmed_at == date of creating
        """

    async def test_creating_user_in_db(
            self,
            created_user_email: str,
            success_response: Response,
            users_repo: UsersRepo
    ):
        user = await users_repo.fetch_by_email(created_user_email)

        assert created_user_email == user.email
        self._test_created_user_claims(user)
