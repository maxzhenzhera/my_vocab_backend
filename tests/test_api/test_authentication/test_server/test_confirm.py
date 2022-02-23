from datetime import timedelta
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

from app.db.models import User
from app.db.repos import UsersRepo
from app.schemas.entities.user import UserInResponse
from ...base import (
    BaseTestRoute,
    BaseTestRouteCase
)
from ...fakers import fake_email_confirmation_token
from ...mixins.response_and_client import ResponseAndClient
from ....utils.datetime_ import assert_datetime


pytestmark = pytest.mark.asyncio


class ConfirmRouteNameMixin:
    route_name: ClassVar[str] = 'auth:confirm'


class TestConfirmRouteSingleCase(
    ConfirmRouteNameMixin,
    BaseTestRouteCase
):
    @property
    def computational_interference(self) -> timedelta:
        """ DB timestamps might slowly differ. """
        return timedelta(seconds=5)

    @pytest.fixture(name='success_params')
    def fixture_success_params(
            self,
            user_1: UserInResponse
    ) -> dict[str, str]:
        return {
            'token': user_1.email_confirmation_token
        }

    @pytest.fixture(name='response_and_client_on_success')
    async def fixture_response_and_client_on_success(
            self,
            route_url: URLPath,
            client_1: AsyncClient,
            success_params: dict[str, str]
    ) -> ResponseAndClient:
        return (
            await client_1.get(
                url=route_url,
                params=success_params
            ),
            client_1
        )

    def test_success_response(self, success_response: Response):
        user = UserInResponse(**success_response.json())

        assert success_response.status_code == HTTP_200_OK
        self._test_email_confirmation_claims(user)

    async def test_updating_user_in_db(
            self,
            success_response: Response,
            users_repo: UsersRepo
    ):
        user_in_response = UserInResponse(**success_response.json())
        user_in_db = await users_repo.fetch_by_email(user_in_response.email)

        self._test_email_confirmation_claims(user_in_db)

    def _test_email_confirmation_claims(self, user: User | UserInResponse):
        assert user.is_email_confirmed
        assert_datetime(
            actual=user.email_confirmed_at,
            delta=self.computational_interference
        )


class TestCommonErrorsOfConfirmRoute(
    ConfirmRouteNameMixin,
    BaseTestRoute
):
    @pytest.fixture(name='bad_params')
    def fixture_bad_params(self) -> dict[str, str]:
        return {
            'token': fake_email_confirmation_token()
        }

    async def test_return_400_error_on_passing_false_link(
            self,
            route_url: URLPath,
            client_1: AsyncClient,
            bad_params: dict[str, str]
    ):
        """
        On confirm has been passed the link
        that does not correspond to the real user email confirmation link.

        Must return 400 Bad Request.
        """

        bad_response = await client_1.get(
            url=route_url,
            params=bad_params
        )

        assert bad_response.status_code == HTTP_400_BAD_REQUEST
