from abc import (
    ABC,
    abstractmethod
)

from httpx import (
    AsyncClient,
    Response
)

from app.db.repositories import UsersRepository
from ...base import BaseTestRoute


__all__ = ['BaseTestCommonUserCreationRoute']


class BaseTestCommonUserCreationRoute(BaseTestRoute, ABC):
    @property
    @abstractmethod
    def created_user_email(self) -> str:
        """
        The created user email.

        Abstract *class* attribute:
            created_user_email: ClassVar[str] = TestUserInCreate.email
        """

    @abstractmethod
    async def test_creating_user_in_db(
            self,
            response: Response,
            test_users_repository: UsersRepository
    ):
        """
        On route execution new user must be created in db.

        User might be created throw:
            1. server (own authentication system);
            2. oauth.

        Server user:
            1. is_email_confirmed == False
            2. email_confirmed_at == None

        OAuth User:
            1. is_email_confirmed == True
            2. email_confirmed_at == date of creating
        """

    @abstractmethod
    async def test_return_400_error_on_passing_already_used_credentials(
            self,
            client: AsyncClient
    ):
        """
        On creation has been passed the same credentials
        (client fixture - client that already sent the same request).

        Must return 400 Bad Request.
        """
