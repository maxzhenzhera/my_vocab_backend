import logging
from dataclasses import dataclass

from fastapi import Depends

from .base import BaseServerAuthenticationService
from ..errors import IncorrectPasswordError
from ...password import PasswordService
from ....api.dependencies.settings import AppSettingsMarker
from ....core.settings import AppSettings
from ....schemas.authentication import AuthenticationResult
from ....schemas.entities.user import (
    UserInCreate,
    UserInLogin
)


__all__ = ['AuthenticationService']


logger = logging.getLogger(__name__)


@dataclass
class AuthenticationService(BaseServerAuthenticationService):
    settings: AppSettings = Depends(AppSettingsMarker)

    async def register(  # type: ignore[override]
            self,
            user_in_create: UserInCreate
    ) -> AuthenticationResult:
        user = await self.user_account_service.register_user(user_in_create)
        return await self.authenticator.authenticate(user)

    async def login(  # type: ignore[override]
            self,
            user_in_login: UserInLogin
    ) -> AuthenticationResult:
        user = await self.user_account_service.fetch_by_email(user_in_login.email)
        if not PasswordService(user).verify(user_in_login.password):
            raise IncorrectPasswordError
        return await self.authenticator.authenticate(user)

    async def refresh(  # type: ignore[override]
            self,
            token: str
    ) -> AuthenticationResult:
        session = await self.authenticator.validate_refresh_session(token)
        user = await self.user_account_service.fetch_by_id(session.user_id)
        return await self.authenticator.authenticate(user)
