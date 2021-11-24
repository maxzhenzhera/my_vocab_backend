from abc import ABC

from httpx import Response
from starlette.status import HTTP_200_OK

from app.db.repositories import RefreshSessionsRepository
from app.services.authentication.cookie import REFRESH_TOKEN_COOKIE_KEY
from ...base import BaseTestRoute


__all__ = ['BaseTestAuthRoute']


class BaseTestAuthRoute(BaseTestRoute, ABC):
    def test_response(self, response: Response):        # noqa Method may be 'static'
        response_json = response.json()

        assert response.status_code == HTTP_200_OK
        assert 'user' in response_json
        assert 'tokens' in response_json

    def test_setting_refresh_token_cookie(self, response: Response):        # noqa Method may be 'static'
        response_json = response.json()

        refresh_token_in_cookie = response.cookies[REFRESH_TOKEN_COOKIE_KEY]
        refresh_token_in_response = response_json['tokens']['refresh_token']['token']

        assert refresh_token_in_cookie == refresh_token_in_response

    async def test_creating_refresh_session_in_db(      # noqa Method may be 'static'
            self,
            response: Response,
            test_refresh_sessions_repository: RefreshSessionsRepository
    ):
        refresh_token = response.cookies[REFRESH_TOKEN_COOKIE_KEY]

        assert await test_refresh_sessions_repository.fetch_by_refresh_token(refresh_token)
