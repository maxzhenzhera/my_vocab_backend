from abc import (
    ABC,
    abstractmethod
)
from dataclasses import (
    dataclass
)

from authlib.integrations.starlette_client import (
    OAuth,
    StarletteRemoteApp
)
from authlib.oidc.core.claims import UserInfo
from fastapi import (
    Depends,
    Request
)

from ..dataclasses_ import OAuthUser
from .....api.dependencies.oauth import OAuthClientMarker
from .....api.dependencies.settings import AppSettingsMarker
from .....core.settings import AppSettings


__all__ = ['BaseAuthorizer']


@dataclass  # type: ignore[misc]
class BaseAuthorizer(ABC):
    request: Request
    settings: AppSettings = Depends(AppSettingsMarker)
    oauth_client: OAuth = Depends(OAuthClientMarker)

    @property
    @abstractmethod
    def oauth_provider_name(self) -> str:
        """ The name of the registered OAuth provider. """

    @property
    def oauth_provider(self) -> StarletteRemoteApp:
        return getattr(self.oauth_client, self.oauth_provider_name)

    async def get_oauth_user(self) -> OAuthUser:
        """
        Implement default building
        of the OAuth user (model with OAuth user info).

        Have to be overridden
        if claims in the provider response
        do not repeat the default behaviour.
        """

        user_info = await self._extract_user_info_from_request()
        return OAuthUser(
            id=user_info.sub,
            email=user_info.email
        )

    async def _extract_user_info_from_request(self) -> UserInfo:
        token = await self.oauth_provider.authorize_access_token(self.request)
        return await self.oauth_provider.parse_id_token(self.request, token)
