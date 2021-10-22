import logging
from dataclasses import dataclass

from fastapi import Depends

from .errors import IncorrectPasswordError
from .request_analyzer import RequestAnalyzer
from .types import RefreshSessionData
from .user_account import UserAccountService
from ...api.dependencies.db import get_repository
from ...db.models import (
    User,
    RefreshSession
)
from ...db.repositories import RefreshSessionsRepository
from ...schemas.authentication import AuthenticationResult
from ...schemas.user import (
    UserInLogin,
    UserInCreate
)
from ...services.jwt import UserJWTService
from ...services.security import UserPasswordService


__all__ = ['AuthenticationService']


logger = logging.getLogger(__name__)


@dataclass
class AuthenticationService:
    request_analyzer: RequestAnalyzer = Depends()
    user_account_service: UserAccountService = Depends()
    refresh_sessions_repository: RefreshSessionsRepository = Depends(get_repository(RefreshSessionsRepository))

    async def register(self, user_in_create: UserInCreate) -> AuthenticationResult:
        user = await self.user_account_service.create_user(user_in_create)
        return await self._authenticate(user)

    async def login(self, user_in_login: UserInLogin) -> AuthenticationResult:
        user = await self.user_account_service.fetch_user_by_email_or_raise_auth_error(user_in_login.email)
        if not UserPasswordService(user).verify_password(user_in_login.password):
            raise IncorrectPasswordError
        return await self._authenticate(user)

    async def _authenticate(self, user: User) -> AuthenticationResult:
        tokens = UserJWTService(user).generate_tokens()
        await self._create_refresh_session(RefreshSessionData(user, tokens.refresh_token))
        return AuthenticationResult(tokens=tokens, user=user) # noqa pydantic by itself make .from_orm() with passed dataclass instance

    async def _create_refresh_session(self, refresh_session_data: RefreshSessionData) -> None:
        await self.refresh_sessions_repository.create_by_entity(
            RefreshSession(
                refresh_token=refresh_session_data.refresh_token.token,
                ip_address=self.request_analyzer.client_ip_address,
                user_agent=self.request_analyzer.client_user_agent,
                expires_at=refresh_session_data.refresh_token.expires_at,
                user_id=refresh_session_data.user.id
            )
        )
