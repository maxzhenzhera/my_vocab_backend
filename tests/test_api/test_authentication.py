import pytest
from httpx import AsyncClient, Response

from app.db.repositories import (
    RefreshSessionsRepository,
    UsersRepository
)
from app.main import app
from app.schemas.user import UserInCreate
from tests.config import mail_connection_test_config


pytestmark = pytest.mark.asyncio


class TestRegisterRoute:
    URL = app.url_path_for('auth:register')
    TEST_USER = UserInCreate(email='example@gmail.com', password='password')    # noqa pydantic email validation
    TEST_JSON = TEST_USER.dict()

    @pytest.fixture(name='response')
    async def response_from_route(self, test_client: AsyncClient) -> Response:
        return await test_client.post(self.URL, json=self.TEST_JSON)

    async def test_route_response(self, response: Response):
        response_json = response.json()

        assert response.status_code == 200
        assert 'user' in response_json and 'tokens' in response_json

    async def test_route_setting_refresh_token_cookie(self, response: Response):
        assert 'refresh_token' in response.cookies

    async def test_register_route_email_sending(self, test_mail_sender, test_client: AsyncClient):
        with test_mail_sender.record_messages() as outbox:
            _ = await test_client.post(self.URL, json=self.TEST_JSON)

            assert len(outbox) == 1
            if mail_connection_test_config.MAIL_FROM_NAME is not None:
                from_ = f"{mail_connection_test_config.MAIL_FROM_NAME} <{mail_connection_test_config.MAIL_FROM}>"
                assert outbox[0]['from'] == from_
            else:
                from_ = mail_connection_test_config.MAIL_FROM
                assert outbox[0]['from'] == from_
            assert outbox[0]['To'] == self.TEST_USER.email

    async def test_route_creating_user_in_db(self, response: Response, test_users_repository: UsersRepository):
        assert await test_users_repository.fetch_by_email(self.TEST_USER.email)

    async def test_route_creating_refresh_session_in_db(self,
                                                        response: Response,
                                                        test_refresh_sessions_repository: RefreshSessionsRepository
                                                        ):
        assert await test_refresh_sessions_repository.fetch_by_refresh_token(response.cookies['refresh_token'])

    async def test_route_return_400_error(self, response: Response, test_client: AsyncClient):
        """ On registration has been passed the same credentials (used fixture) - must return 400 Bad Request """
        response = await test_client.post(self.URL, json=self.TEST_JSON)
        assert response.status_code == 400
