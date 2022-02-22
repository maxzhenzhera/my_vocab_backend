from typing import ClassVar

import pytest
from httpx import AsyncClient
from starlette.datastructures import URLPath

from app.db.repositories import OAuthConnectionsRepo
from app.__main__ import app
from app.schemas.authentication import AuthenticationResult
from app.schemas.authentication.oauth import OAuthUser
from ..base import BaseOauthLoginRoute
from tests.test_api.users import user_1


pytestmark = pytest.mark.asyncio


class TestGoogleLoginRoute(BaseOauthLoginRoute):
    url: ClassVar[URLPath] = app.url_path_for('oauth:google:login')
    oauth_user: ClassVar[OAuthUser] = user_1.google_oauth_user

    @pytest.mark.usefixtures('mock_get_oauth_user')
    async def test_creating_oauth_connection_in_db_on_existed_user_login(
            self,
            test_oauth_connections_repository: OAuthConnectionsRepo,
            test_unauthenticated_client_user_1: AsyncClient
    ):
        response = await test_unauthenticated_client_user_1.get(self.url)
        authenticated_user = AuthenticationResult(**response.json()).user

        google_oauth_connection = await (
            test_oauth_connections_repository
            .fetch_by_google_id_with_user(self.oauth_user.id)
        )

        assert google_oauth_connection.user_id == authenticated_user.id
