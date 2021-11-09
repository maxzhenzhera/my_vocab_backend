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

from app.db.errors import EntityDoesNotExistError
from app.db.repositories import (
    RefreshSessionsRepository,
    UsersRepository
)
from app.main import app
from app.services.authentication.cookie import REFRESH_TOKEN_COOKIE_KEY
from tests.config import mail_connection_test_config
from tests.helpers.auth import get_user_from_client
from tests.users import test_user_1


pytestmark = pytest.mark.asyncio


class ResponseAndClientFixturesMixin:
    @pytest.fixture(name='response')
    def fixture_response(self, response_and_client: tuple[Response, AsyncClient]) -> Response:
        return response_and_client[0]

    @pytest.fixture(name='client')
    def fixture_client(self, response_and_client: tuple[Response, AsyncClient]) -> AsyncClient:
        return response_and_client[1]


class AuthRouteMixin:
    URL: URLPath
    JSON: dict

    def test_route_response(self, response: Response):                          # noqa method may be static
        response_json = response.json()

        assert response.status_code == HTTP_200_OK
        assert 'user' in response_json
        assert 'tokens' in response_json

    def test_route_setting_refresh_token_cookie(self, response: Response):      # noqa method may be static
        response_json = response.json()

        assert response.cookies[REFRESH_TOKEN_COOKIE_KEY] == response_json['tokens']['refresh_token']['token']

    async def test_route_creating_refresh_session_in_db(                        # noqa method may be static
            self,
            response: Response,
            test_refresh_sessions_repository: RefreshSessionsRepository
    ):
        assert await test_refresh_sessions_repository.fetch_by_refresh_token(response.cookies[REFRESH_TOKEN_COOKIE_KEY])


class UserCreationRouteMixin:
    URL: URLPath
    JSON: dict
    USER_EMAIL: str

    async def test_route_creating_user_in_db(
            self,
            response: Response,         # noqa Parameter 'response' value is not used (use fixture)
            test_users_repository: UsersRepository
    ):
        assert await test_users_repository.fetch_by_email(self.USER_EMAIL)

    async def test_route_return_400_error_on_passing_already_used_credentials(self, client: AsyncClient):
        """
        On creation has been passed the same credentials (client fixture - client that already sent the same request).
        Must return 400 Bad Request.
        """

        response = await client.post(self.URL, json=self.JSON)
        assert response.status_code == HTTP_400_BAD_REQUEST


class TerminatingRefreshSessionRouteMixin:
    @pytest.fixture(name='old_refresh_token')
    def fixture_refresh_token(self, test_client_user_1: AsyncClient) -> str:
        return test_client_user_1.cookies[REFRESH_TOKEN_COOKIE_KEY]

    async def test_route_deleting_refresh_session_from_db(                      # noqa method may be static
            self,
            old_refresh_token: str,
            response: Response,         # noqa Parameter 'response' value is not used (use fixture)
            test_refresh_sessions_repository: RefreshSessionsRepository
    ):
        """
        The order of the used fixtures is important.
        If put < refresh_token > after < response > than it would be a try to get the cookie from the logged out user.
        """

        with pytest.raises(EntityDoesNotExistError):
            await test_refresh_sessions_repository.fetch_by_refresh_token(old_refresh_token)


class TestCreateRoute(UserCreationRouteMixin, ResponseAndClientFixturesMixin):
    URL = app.url_path_for('auth:create')
    JSON = test_user_1.in_create.dict()
    USER_EMAIL = test_user_1.email

    @pytest.fixture(name='response_and_client')
    async def fixture_response_and_client(self, test_client: AsyncClient) -> tuple[Response, AsyncClient]:
        return await test_client.post(self.URL, json=self.JSON), test_client


class TestRegisterRoute(AuthRouteMixin, UserCreationRouteMixin, ResponseAndClientFixturesMixin):
    URL = app.url_path_for('auth:register')
    JSON = test_user_1.in_create.dict()
    USER_EMAIL = test_user_1.email

    @pytest.fixture(name='response_and_client')
    async def fixture_response_and_client(self, test_client: AsyncClient) -> tuple[Response, AsyncClient]:
        return await test_client.post(self.URL, json=self.JSON), test_client

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


class TestLoginRoute(AuthRouteMixin):
    URL = app.url_path_for('auth:login')
    JSON = test_user_1.in_login.dict()

    @pytest.fixture(name='response')
    async def fixture_response_from_route(self, test_unauthenticated_client_user_1: AsyncClient) -> Response:
        return await test_unauthenticated_client_user_1.post(self.URL, json=self.JSON)

    async def test_route_return_401_error_on_passing_false_credentials(self, test_client: AsyncClient):
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

    def test_route_response(self, response: Response):
        response_json = response.json()

        assert response.status_code == HTTP_200_OK
        assert response_json['is_email_confirmed']
        assert datetime.utcnow() - datetime.fromisoformat(response_json['email_confirmed_at']) < timedelta(seconds=10)

    async def test_route_updating_user_in_db(self, response: Response, test_users_repository: UsersRepository):
        user = await test_users_repository.fetch_by_email(self.USER_EMAIL)

        assert user.is_email_confirmed
        assert datetime.utcnow() - user.email_confirmed_at < timedelta(seconds=10)

    async def test_route_return_400_error_on_passing_false_link(self, params: dict, test_client_user_1: AsyncClient):
        """
        On confirm has been passed the link that does not correspond to the real user email confirmation link.
        Must return 400 Bad Request.
        """

        params['link'] = uuid4()
        response = await test_client_user_1.get(self.URL, params=params)

        assert response.status_code == HTTP_400_BAD_REQUEST


class TestLogoutRoute(TerminatingRefreshSessionRouteMixin, ResponseAndClientFixturesMixin):
    URL = app.url_path_for('auth:logout')

    @pytest.fixture(name='response_and_client')
    async def fixture_response_and_client(self, test_client_user_1: AsyncClient) -> tuple[Response, AsyncClient]:
        return await test_client_user_1.get(self.URL), test_client_user_1

    def test_route_response(self, response: Response):
        response_json = response.json()

        assert response.status_code == HTTP_200_OK
        assert response_json is None

    def test_route_deleting_refresh_token_cookie(self, client: AsyncClient):
        assert REFRESH_TOKEN_COOKIE_KEY not in client.cookies


class TestRefreshRoute(AuthRouteMixin, TerminatingRefreshSessionRouteMixin, ResponseAndClientFixturesMixin):
    URL = app.url_path_for('auth:refresh')

    @pytest.fixture(name='response_and_client')
    async def fixture_response_and_client(self, test_client_user_1: AsyncClient) -> tuple[Response, AsyncClient]:
        return await test_client_user_1.get(self.URL), test_client_user_1

    def test_route_deleting_old_refresh_token_cookie(self, old_refresh_token: str, client: AsyncClient):
        assert client.cookies[REFRESH_TOKEN_COOKIE_KEY] != old_refresh_token

    async def test_route_return_401_error_on_expired_session(
            self,
            old_refresh_token: str,
            test_client_user_1: AsyncClient,
            test_refresh_sessions_repository: RefreshSessionsRepository
    ):
        """
        On refresh has been passed refresh token which session has manually expired.
        Must return 401 Unauthorized.
        """

        await test_refresh_sessions_repository.expire(old_refresh_token)
        await test_refresh_sessions_repository.session.commit()
        response = await test_client_user_1.get('/api/auth/refresh')

        assert response.status_code == HTTP_401_UNAUTHORIZED

    async def test_route_return_401_error_on_passing_false_refresh_token(self, test_client_user_1: AsyncClient):
        """
        On confirm has been passed the link that does not correspond to the real user email confirmation link.
        Must return 401 Unauthorized.
        """

        test_client_user_1.cookies[REFRESH_TOKEN_COOKIE_KEY] = str(uuid4())
        response = await test_client_user_1.get(self.URL)

        assert response.status_code == HTTP_401_UNAUTHORIZED
