from abc import ABC

from httpx import Response
from starlette.status import HTTP_200_OK

from app.db.repos import RefreshSessionsRepo
from app.schemas.authentication import AuthenticationResult
from app.services.authentication.authenticator.cookie import REFRESH_TOKEN_COOKIE_KEY
from ...base import BaseTestRouteCase


__all__ = ['BaseTestAuthRouteCase']


class BaseTestAuthRouteCase(BaseTestRouteCase, ABC):
    def test_success_response(self, success_response: Response):
        response_json = success_response.json()

        assert success_response.status_code == HTTP_200_OK
        assert 'user' in response_json
        assert 'tokens' in response_json

    def test_setting_refresh_token_cookie(self, success_response: Response):
        authentication_result = AuthenticationResult(**success_response.json())

        refresh_token_in_cookie = success_response.cookies[REFRESH_TOKEN_COOKIE_KEY]
        refresh_token_in_response = authentication_result.refresh_token

        assert refresh_token_in_cookie == refresh_token_in_response

    async def test_creating_refresh_session_in_db(
            self,
            success_response: Response,
            refresh_sessions_repo: RefreshSessionsRepo
    ):
        refresh_token = success_response.cookies[REFRESH_TOKEN_COOKIE_KEY]

        assert await refresh_sessions_repo.exists_by_token(refresh_token)
