import pytest

from app.db.models import OAuthConnection
from app.db.repos import OAuthConnectionsRepo
from app.services.authentication.oauth.dataclasses_ import OAuthUser
from ...protocols import HasUsedMetaUserFixture
from .....dataclasses_ import MetaUser


__all__ = ['GoogleOAuthFixturesMixin']


class GoogleOAuthFixturesMixin:
    @pytest.fixture(name='oauth_user')
    def fixture_oauth_user(
            self: HasUsedMetaUserFixture,
            used_meta_user: MetaUser
    ) -> OAuthUser:
        return used_meta_user.google_oauth_user

    async def _fetch_oauth_connection(
            self,
            oauth_user: OAuthUser,
            repo: OAuthConnectionsRepo,
    ) -> OAuthConnection:
        return await repo.fetch_by_google_id(oauth_user.id)
