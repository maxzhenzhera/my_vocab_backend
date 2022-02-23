from ..base.service import BaseOAuthService
from ..dataclasses_ import OAuthUser
from .....db.models import (
    OAuthConnection,
    User
)


__all__ = ['GoogleOAuthService']


class GoogleOAuthService(BaseOAuthService):
    async def _fetch_oauth_connection(self, oauth_user: OAuthUser) -> OAuthConnection:
        return await self.oauth_connections_repo.fetch_by_google_id(oauth_user.id)

    async def _link_oauth_connection_to_user(
            self,
            oauth_user: OAuthUser,
            internal_user: User
    ) -> None:
        await self.oauth_connections_repo.link_google_connection(
            oauth_user=oauth_user,
            internal_user=internal_user
        )
