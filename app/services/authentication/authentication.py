import logging
from dataclasses import dataclass

from fastapi import Depends

from .errors import IncorrectPasswordError
from .refresh_session import RefreshSessionService
from .user_account import UserAccountService
from ...schemas.authentication import AuthenticationResult
from ...schemas.user import (
    UserInLogin,
    UserInCreate
)
from ...services.security import UserPasswordService


__all__ = ['AuthenticationService']


logger = logging.getLogger(__name__)


@dataclass
class AuthenticationService:
    user_account_service: UserAccountService = Depends()
    refresh_session_service: RefreshSessionService = Depends()

    async def register(self, user_in_create: UserInCreate) -> AuthenticationResult:
        user = await self.user_account_service.create_user(user_in_create)
        return await self.refresh_session_service.authenticate(user)

    async def login(self, user_in_login: UserInLogin) -> AuthenticationResult:
        user = await self.user_account_service.fetch_user_by_email_or_raise_auth_error(user_in_login.email)
        if not UserPasswordService(user).verify_password(user_in_login.password):
            raise IncorrectPasswordError
        return await self.refresh_session_service.authenticate(user)

    async def refresh(self, refresh_token: str) -> AuthenticationResult:
        refresh_session = await self.refresh_session_service.validate_refresh_session(refresh_token)
        user = await self.user_account_service.users_repository.fetch_by_id(refresh_session.user_id)
        return await self.refresh_session_service.authenticate(user)
