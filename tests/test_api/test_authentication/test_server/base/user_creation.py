from abc import ABC

from httpx import (
    AsyncClient,
    Response
)
from starlette.status import HTTP_400_BAD_REQUEST

from app.db.repos import UsersRepo


__all__ = ['UserCreationTestsMixin']


class UserCreationTestsMixin(BaseTestUserCreationRoute):
    async def test_creating_user_in_db(
            self,
            response: Response,
            test_users_repository: UsersRepository
    ):
        user = await test_users_repository.fetch_by_email(self.created_user_email)

        assert not user.is_email_confirmed
        assert user.email_confirmed_at is None

    async def test_return_400_error_on_passing_already_used_credentials(
            self,
            client: AsyncClient
    ):
        response = await client.post(self.url, json=self.request_json)

        assert response.status_code == HTTP_400_BAD_REQUEST
