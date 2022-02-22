import logging
from dataclasses import dataclass

from .base import BaseServerAuthenticationService
from ..errors import IncorrectPasswordError
from ...security import UserPasswordService
from ....schemas.authentication import AuthenticationResult
from ....schemas.entities.user import (
    UserInLogin,
    UserInCreate
)

__all__ = ['AuthenticationService']


logger = logging.getLogger(__name__)


@dataclass
class AuthenticationService(BaseServerAuthenticationService):
    async def register(self, user_in_create: UserInCreate) -> AuthenticationResult:
        user = await self.user_account_service.register_user(user_in_create)
        return await self.refresh_session_service.authenticate(user)

    async def login(self, user_in_login: UserInLogin) -> AuthenticationResult:
        user = await self.user_account_service.fetch_user(user_in_login.email)
        if not UserPasswordService(user).verify_password(user_in_login.password):
            raise IncorrectPasswordError
        return await self.refresh_session_service.authenticate(user)

    async def refresh(self, refresh_token: str) -> AuthenticationResult:
        refresh_session = await self.refresh_session_service.validate_refresh_session(refresh_token)
        user = await self.user_account_service.users_repository.fetch_by_id(refresh_session.user_id)
        return await self.refresh_session_service.authenticate(user)