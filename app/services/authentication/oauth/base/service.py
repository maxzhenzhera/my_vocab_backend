from abc import abstractmethod
from dataclasses import dataclass

from fastapi import Depends

from ..dataclasses_ import (
    OAuthUser,
    OAuthUserCredentials
)
from ...base import BaseAuthenticationService
from ...errors import OAuthConnectionDoesNotExistError
from .....db.errors import EntityDoesNotExistError
from .....db.models import (
    OAuthConnection,
    User
)
from .....db.repos import OAuthConnectionsRepo
from .....schemas.authentication import AuthenticationResult


__all__ = ['BaseOAuthService']


@dataclass  # type: ignore[misc]
class BaseOAuthService(BaseAuthenticationService):
    oauth_connections_repo: OAuthConnectionsRepo = Depends()

    async def register(  # type: ignore[override]
            self,
            oauth_user: OAuthUser
    ) -> tuple[AuthenticationResult, OAuthUserCredentials]:
        user, credentials = await self.user_account_service.register_oauth_user(oauth_user)  # noqa: E501
        bound_user = await self._bind_oauth_connection_to_user(oauth_user, user)
        authentication_result = await self.authenticator.authenticate(bound_user)
        return authentication_result, credentials

    async def login(  # type: ignore[override]
            self,
            oauth_user: OAuthUser
    ) -> AuthenticationResult:
        try:
            authentication_result = await self._login_via_connection(oauth_user)
        except OAuthConnectionDoesNotExistError:
            authentication_result = await self._login_via_email(oauth_user)
        return authentication_result

    async def _login_via_connection(
            self,
            oauth_user: OAuthUser
    ) -> AuthenticationResult:
        try:
            oauth_connection = await self._fetch_oauth_connection(oauth_user)
        except EntityDoesNotExistError as error:
            raise OAuthConnectionDoesNotExistError from error
        else:
            return await self.authenticator.authenticate(oauth_connection.user)

    @abstractmethod
    async def _fetch_oauth_connection(
            self,
            oauth_user: OAuthUser
    ) -> OAuthConnection:
        """
        Fetch OAuth connection by OAuth user.

        Related db repo method have to be used.
        """

    async def _login_via_email(
            self,
            oauth_user: OAuthUser
    ) -> AuthenticationResult:
        user = await self.user_account_service.fetch_by_email(oauth_user.email)
        bound_user = await self._bind_oauth_connection_to_user(oauth_user, user)
        return await self.authenticator.authenticate(bound_user)

    async def _bind_oauth_connection_to_user(
            self,
            oauth_user: OAuthUser,
            internal_user: User
    ) -> User:
        await self._link_oauth_connection_to_user(oauth_user, internal_user)
        confirmed_user = await self.user_account_service.confirm_email(internal_user)
        return confirmed_user

    @abstractmethod
    async def _link_oauth_connection_to_user(
            self,
            oauth_user: OAuthUser,
            internal_user: User
    ) -> None:
        """
        Link OAuth connection to the internal user.

        Related db repo method have to be used.
        """
