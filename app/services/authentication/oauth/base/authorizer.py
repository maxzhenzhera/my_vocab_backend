from abc import (
    ABC,
    abstractmethod
)
from dataclasses import dataclass

from authlib.integrations.starlette_client import StarletteOAuth2App
from authlib.oidc.core.claims import UserInfo
from fastapi import Request

from ..dataclasses_ import OAuthUser


__all__ = ['BaseAuthorizer']


@dataclass  # type: ignore[misc]
class BaseAuthorizer(ABC):
    request: Request

    @property
    @abstractmethod
    def oauth_provider(self) -> StarletteOAuth2App:
        """
        OAuth provider of authorizer
        that have to be declared in subclass
        as dependency.
        """

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
