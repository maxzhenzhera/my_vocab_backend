from datetime import (
    datetime,
    timedelta
)
from typing import ClassVar

import pytest
from httpx import (
    AsyncClient,
    Response
)
from starlette.datastructures import URLPath
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST
)

from app.db.repositories import UsersRepository
from app.main import app
from app.schemas.entities.user import UserInResponse
from ....base import BaseTestRoute
from ....mixins.response_and_client import ResponseAndClient
from .....helpers.auth import get_user_from_client
from .....helpers.email_confirmation_link import generate_fake_email_confirmation_link


pytestmark = pytest.mark.asyncio


class TestConfirmRoute(BaseTestRoute):
    url: ClassVar[URLPath] = app.url_path_for('auth:confirm')

    @pytest.fixture(name='params')
    def fixture_params(self, test_client_user_1: AsyncClient) -> dict[str, str]:
        return {
            'link': get_user_from_client(test_client_user_1).email_confirmation_link
        }

    @pytest.fixture(name='response_and_client')
    async def fixture_response_and_client(
            self,
            params: dict[str, str],
            test_client_user_1: AsyncClient
    ) -> ResponseAndClient:
        return await test_client_user_1.get(self.url, params=params), test_client_user_1

    def test_response(self, response: Response):
        user_in_response = UserInResponse(**response.json())

        assert response.status_code == HTTP_200_OK
        self._test_email_confirmation_claims(
            user_in_response.is_email_confirmed,
            user_in_response.email_confirmed_at
        )

    async def test_updating_user_in_db(
            self,
            response: Response,
            test_users_repository: UsersRepository
    ):
        user_in_response = UserInResponse(**response.json())
        user_in_db = await test_users_repository.fetch_by_email(user_in_response.email)

        self._test_email_confirmation_claims(
            user_in_db.is_email_confirmed,
            user_in_db.email_confirmed_at
        )

    @staticmethod
    def _test_email_confirmation_claims(
            is_email_confirmed: bool,
            email_confirmed_at: datetime
    ):
        assert is_email_confirmed
        assert datetime.utcnow() - email_confirmed_at < timedelta(seconds=10)

    async def test_return_400_error_on_passing_false_link(
            self,
            params: dict,
            test_client_user_1: AsyncClient
    ):
        """
        On confirm has been passed the link
        that does not correspond to the real user email confirmation link.

        Must return 400 Bad Request.
        """

        params['link'] = generate_fake_email_confirmation_link()
        response = await test_client_user_1.get(self.url, params=params)

        assert response.status_code == HTTP_400_BAD_REQUEST
