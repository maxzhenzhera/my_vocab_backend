from ..base.oauth import BaseOAuthService

from .....db.models import (
    User,
    OAuthConnection
)
from .....schemas.authentication.oauth import (
    GoogleOAuthConnection,
    OAuthUser
)


__all__ = ['GoogleOAuthService']


class GoogleOAuthService(BaseOAuthService):
    async def _fetch_oauth_connection(self, oauth_user: OAuthUser) -> OAuthConnection:
        return await self.oauth_connections_repository.fetch_by_google_id_with_user(oauth_user.id)

    def _build_oauth_connection_instance(
            self,
            oauth_user: OAuthUser,
            internal_user: User
    ) -> GoogleOAuthConnection:
        return GoogleOAuthConnection(
            user_id=internal_user.id,
            google_id=oauth_user.id
        )
