from abc import ABC
from datetime import (
    datetime,
    timedelta
)

from httpx import Response

from app.db.repositories import UsersRepository
from ...base import BaseTestCommonUserCreationRoute


__all__ = ['BaseTestOAuthUserCreationRoute']


class BaseTestOAuthUserCreationRoute(BaseTestCommonUserCreationRoute, ABC):
    async def test_creating_user_in_db(
            self,
            response: Response,
            test_users_repository: UsersRepository
    ):
        user = await test_users_repository.fetch_by_email(self.created_user_email)

        assert user.is_email_confirmed
        assert datetime.utcnow() - user.email_confirmed_at < timedelta(seconds=5)
