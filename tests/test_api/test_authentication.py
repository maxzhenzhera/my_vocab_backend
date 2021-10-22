from datetime import (
    datetime,
    timedelta
)
from uuid import uuid4

import pytest
from httpx import (
    AsyncClient,
    Response
)
from starlette.datastructures import URLPath
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED
)

from app.db.repositories import (
    RefreshSessionsRepository,
    UsersRepository
)
from app.main import app
from tests.config import mail_connection_test_config
from tests.users import test_user_1
from tests.helpers.auth import get_user_from_client


pytestmark = pytest.mark.asyncio


class RegisterAndLoginRoutesMixin:
    URL: URLPath
    JSON: dict

    async def test_route_response(self, response: Response):                        # noqa method may be static
        response_json = response.json()

        assert response.status_code == HTTP_200_OK
        assert 'user' in response_json and 'tokens' in response_json

    async def test_route_setting_refresh_token_cookie(self, response: Response):    # noqa method may be static
        assert 'refresh_token' in response.cookies

    async def test_route_creating_refresh_session_in_db(                            # noqa method may be static
            self,
            response: Response,
            test_refresh_sessions_repository: RefreshSessionsRepository
    ):
        assert await test_refresh_sessions_repository.fetch_by_refresh_token(response.cookies['refresh_token'])


class CreateAndRegisterRoutesMixin:
    URL: URLPath
    JSON: dict
    USER_EMAIL: str

    async def test_route_creating_user_in_db(self, response: Response, test_users_repository: UsersRepository):
        assert await test_users_repository.fetch_by_email(self.USER_EMAIL)

    async def test_route_return_400_error(self, response: Response, test_client: AsyncClient):
        """
        On creation has been passed the same credentials (used fixture).
        Must return 400 Bad Request.
        """
        response = await test_client.post(self.URL, json=self.JSON)
        assert response.status_code == HTTP_400_BAD_REQUEST


class TestCreateRoute(CreateAndRegisterRoutesMixin):
    URL = app.url_path_for('auth:create')
    JSON = test_user_1.in_create.dict()
    USER_EMAIL = test_user_1.email

    @pytest.fixture(name='response')
    async def fixture_response(self, test_client: AsyncClient) -> Response:
        return await test_client.post(self.URL, json=self.JSON)


class TestRegisterRoute(RegisterAndLoginRoutesMixin, CreateAndRegisterRoutesMixin):
    URL = app.url_path_for('auth:register')
    JSON = test_user_1.in_create.dict()
    USER_EMAIL = test_user_1.email

    @pytest.fixture(name='response')
    async def fixture_response(self, test_client: AsyncClient) -> Response:
        return await test_client.post(self.URL, json=self.JSON)

    async def test_register_route_email_sending(self, test_mail_sender, test_client: AsyncClient):
        with test_mail_sender.record_messages() as outbox:
            _ = await test_client.post(self.URL, json=self.JSON)

            assert len(outbox) == 1
            if mail_connection_test_config.MAIL_FROM_NAME is not None:
                from_ = f"{mail_connection_test_config.MAIL_FROM_NAME} <{mail_connection_test_config.MAIL_FROM}>"
                assert outbox[0]['from'] == from_
            else:
                from_ = mail_connection_test_config.MAIL_FROM
                assert outbox[0]['from'] == from_
            assert outbox[0]['To'] == self.USER_EMAIL


class TestLoginRoute(RegisterAndLoginRoutesMixin):
    URL = app.url_path_for('auth:login')
    JSON = test_user_1.in_login.dict()

    @pytest.fixture(name='response')
    async def fixture_response_from_route(self, test_unauthenticated_client_user_1: AsyncClient) -> Response:
        return await test_unauthenticated_client_user_1.post(self.URL, json=self.JSON)

    async def test_route_return_401_error(self, test_client: AsyncClient):
        """
        On login has been passed the credentials of the nonexistent user.
        Must return 401 Unauthorized.
        """
        response = await test_client.post(self.URL, json=self.JSON)
        assert response.status_code == HTTP_401_UNAUTHORIZED


class TestConfirmRoute:
    URL = app.url_path_for('auth:confirm')
    USER_EMAIL = test_user_1.email

    @pytest.fixture(name='params')
    def fixture_params(self, test_client_user_1: AsyncClient) -> dict:
        return {
            'link': get_user_from_client(test_client_user_1).email_confirmation_link
        }

    @pytest.fixture(name='response')
    async def fixture_response_from_route(self, params: dict, test_client_user_1: AsyncClient) -> Response:
        return await test_client_user_1.get(self.URL, params=params)

    async def test_route_response(self, response: Response):
        response_json = response.json()

        assert response.status_code == HTTP_200_OK
        assert 'email' in response_json
        assert response_json['is_email_confirmed']
        assert datetime.utcnow() - datetime.fromisoformat(response_json['email_confirmed_at']) < timedelta(seconds=10)

    async def test_route_updating_user_in_db(self, response: Response, test_users_repository: UsersRepository):
        user = await test_users_repository.fetch_by_email(self.USER_EMAIL)

        assert user.is_email_confirmed
        assert datetime.utcnow() - user.email_confirmed_at < timedelta(seconds=10)

    async def test_route_return_400_error(self, params: dict, test_client_user_1: AsyncClient):
        """
        On confirm has been passed the link that does not correspond to the real user email confirmation link.
        Must return 400 Bad Request.
        """
        params['link'] = uuid4()
        response = await test_client_user_1.get(self.URL, params=params)

        assert response.status_code == HTTP_400_BAD_REQUEST
