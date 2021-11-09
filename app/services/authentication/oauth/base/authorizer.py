from abc import (
    ABC,
    abstractmethod
)
from dataclasses import dataclass

from authlib.integrations.starlette_client import StarletteRemoteApp
from authlib.oidc.core.claims import UserInfo
from fastapi import Request

from ..client import oauth
from .....schemas.authentication.oauth.user import OAuthUser


__all__ = ['BaseAuthorizer']


@dataclass
class BaseAuthorizer(ABC):
    request: Request

    @property
    @abstractmethod
    def oauth_service_name(self) -> str:
        """
        Get the oauth service name passed on the oauth registration.

        .. code-block:: python

            oauth.register(
                name=service_name,      # <--------------------
                ...
            )
        """

    @property
    def oauth_service(self) -> StarletteRemoteApp:
        return getattr(oauth, self.oauth_service_name)

    async def get_oauth_user(self):
        user_info = await self._extract_user_info_from_request()
        return OAuthUser(
            id=user_info.sub,
            email=user_info.email
        )

    async def _extract_user_info_from_request(self) -> UserInfo:
        token = await self.oauth_service.authorize_access_token(self.request)
        return await self.oauth_service.parse_id_token(self.request, token)
