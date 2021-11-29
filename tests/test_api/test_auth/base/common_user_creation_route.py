from abc import (
    ABC,
    abstractmethod
)

from httpx import (
    AsyncClient,
    Response
)
from starlette.status import HTTP_400_BAD_REQUEST

from app.db.repositories import UsersRepository
from ...base import BaseTestPostRoute


__all__ = ['BaseTestUserCreationRoute']


class BaseTestUserCreationRoute(BaseTestPostRoute, ABC):
    @property
    @abstractmethod
    def created_user_email(self) -> str:
        """
        The created user email.

        Abstract *class* attribute:
            created_user_email: ClassVar[str] = TestUserInCreate.email
        """

    async def test_creating_user_in_db(
            self,
            response: Response,
            test_users_repository: UsersRepository
    ):
        assert await test_users_repository.fetch_by_email(self.created_user_email)

    async def test_return_400_error_on_passing_already_used_credentials(
            self,
            client: AsyncClient
    ):
        """
        On creation has been passed the same credentials
        (client fixture - client that already sent the same request).

        Must return 400 Bad Request.
        """

        response = await client.post(self.url, json=self.request_json)

        assert response.status_code == HTTP_400_BAD_REQUEST
