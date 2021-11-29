from typing import ClassVar

import pytest
from httpx import Response
from starlette.datastructures import URLPath

from app.db.repositories import OAuthConnectionsRepository
from app.main import app
from app.schemas.authentication import AuthenticationResult
from app.schemas.authentication.oauth import OAuthUser
from ..base import BaseOauthRegisterRoute
from .....users import test_user_1


pytestmark = pytest.mark.asyncio


class TestGoogleRegisterRoute(BaseOauthRegisterRoute):
    url: ClassVar[URLPath] = app.url_path_for('oauth:google:register')
    oauth_user: ClassVar[OAuthUser] = test_user_1.google_oauth_user
    created_user_email: ClassVar[str] = test_user_1.email

    @pytest.mark.usefixtures('mock_get_oauth_user')
    async def test_creating_oauth_connection_in_db(
            self,
            test_oauth_connections_repository: OAuthConnectionsRepository,
            response: Response,
    ):
        created_user = AuthenticationResult(**response.json()).user

        google_oauth_connection = await (
            test_oauth_connections_repository
            .fetch_by_google_id_with_user(self.oauth_user.id)
        )

        assert google_oauth_connection.user_id == created_user.id
