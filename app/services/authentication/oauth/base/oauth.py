from abc import abstractmethod
from dataclasses import dataclass

from fastapi import Depends

from ...errors import OAuthConnectionDoesNotExistError
from ...base import BaseAuthenticationService
from .....api.dependencies.db import get_repository
from .....db.errors import EntityDoesNotExistError
from .....db.models import (
    User,
    OAuthConnection
)
from .....db.repositories import OAuthConnectionsRepository
from .....schemas.authentication import AuthenticationResult
from .....schemas.authentication.oauth import (
    OAuthRegistrationResult,
    BaseOAuthConnection,
    OAuthUser
)
from .....schemas.entities.user import UserInLogin


__all__ = ['BaseOAuthService']


@dataclass
class BaseOAuthService(BaseAuthenticationService):
    oauth_connections_repository: OAuthConnectionsRepository = Depends(get_repository(OAuthConnectionsRepository))

    async def register(self, oauth_user: OAuthUser) -> OAuthRegistrationResult:
        user_in_create = self.user_account_service.generate_in_create_schema_for_oauth_user(oauth_user)
        user = await self.user_account_service.register_oauth_user(user_in_create)
        bound_user = await self._bind_oauth_connection_to_user(oauth_user, user)
        authentication_result = await self.refresh_session_service.authenticate(bound_user)
        return OAuthRegistrationResult(
            authentication_result=authentication_result,
            credentials=UserInLogin(**user_in_create.dict())
        )

    async def login(self, oauth_user: OAuthUser) -> AuthenticationResult:
        try:
            authentication_result = await self._login_by_oauth_connection(oauth_user)
        except OAuthConnectionDoesNotExistError:
            authentication_result = await self._login_by_oauth_email(oauth_user)
        return authentication_result

    async def _login_by_oauth_connection(self, oauth_user: OAuthUser) -> AuthenticationResult:
        try:
            oauth_connection = await self._fetch_oauth_connection(oauth_user)
        except EntityDoesNotExistError as error:
            raise OAuthConnectionDoesNotExistError from error
        else:
            return await self.refresh_session_service.authenticate(oauth_connection.user)

    @abstractmethod
    async def _fetch_oauth_connection(self, oauth_user: OAuthUser) -> OAuthConnection:
        """ Fetch OAuth connection by OAuth user id. """

    async def _login_by_oauth_email(self, oauth_user: OAuthUser) -> AuthenticationResult:
        user = await self.user_account_service.fetch_user_by_email_or_raise_auth_error(oauth_user.email)
        bound_user = await self._bind_oauth_connection_to_user(oauth_user, user)
        return await self.refresh_session_service.authenticate(bound_user)

    async def _bind_oauth_connection_to_user(self, oauth_user: OAuthUser, internal_user: User) -> User:
        await self._link_oauth_connection_to_user(oauth_user, internal_user)
        confirmed_user = await self._confirm_user_email(internal_user)
        return confirmed_user

    async def _link_oauth_connection_to_user(self, oauth_user: OAuthUser, internal_user: User) -> None:
        oauth_connection = self._build_oauth_connection_instance(oauth_user, internal_user)
        await self.oauth_connections_repository.link_connection(oauth_connection)

    @abstractmethod
    def _build_oauth_connection_instance(self, oauth_user: OAuthUser, internal_user: User) -> BaseOAuthConnection:
        """
        Build OAuth connection instance that contains:
            1. internal user id;
            2. OAuth user id.
        """

    async def _confirm_user_email(self, user: User) -> User:
        if user.is_email_confirmed:
            return user
        return await self.user_account_service.users_repository.confirm_by_email(user.email)
