import logging
from dataclasses import dataclass
from typing import ClassVar

from fastapi import Depends

from .cookie import CookieService
from .request_analyzer import RequestAnalyzer
from ..errors import (
    RefreshSessionDoesNotExistError,
    RefreshSessionExpiredError
)
from ...jwt import JWTService
from ....core.config import get_app_settings
from ....core.settings import AppSettings
from ....db.models import (
    RefreshSession,
    User
)
from ....db.repos import RefreshSessionsRepo
from ....schemas.authentication import (
    AuthenticationResult,
    TokenInResponse,
    TokensInResponse
)


__all__ = ['Authenticator']


logger = logging.getLogger(__name__)


@dataclass
class Authenticator:
    settings: ClassVar[AppSettings] = get_app_settings()

    request_analyzer: RequestAnalyzer = Depends()
    refresh_sessions_repo: RefreshSessionsRepo = Depends()
    cookie_service: CookieService = Depends()

    async def authenticate(self, user: User) -> AuthenticationResult:
        refresh_session = await self._create_refresh_session(user)
        self.cookie_service.set_refresh_token(refresh_session.token)
        return AuthenticationResult(
            tokens=self._form_tokens(
                user=user,
                refresh_session=refresh_session
            ),
            user=user
        )

    async def _create_refresh_session(self, user: User) -> RefreshSession:
        return await self.refresh_sessions_repo.create_by_entity(
            RefreshSession(
                user_id=user.id,
                ip_addr=self.request_analyzer.client_ip_address,
                user_agent=self.request_analyzer.client_user_agent
            )
        )

    def _form_tokens(
            self,
            user: User,
            refresh_session: RefreshSession
    ) -> TokensInResponse:
        return TokensInResponse(
            access_token=self._form_access_token(user),
            refresh_token=self._form_refresh_token(refresh_session)
        )

    def _form_access_token(self, user: User) -> TokenInResponse:
        return TokenInResponse(
            token=JWTService(user).access_token.generate(),
            token_type=self.settings.jwt.access_token.type,
            ttl=self.settings.jwt.access_token.expire_in_seconds
        )

    def _form_refresh_token(self, refresh_session: RefreshSession) -> TokenInResponse:
        return TokenInResponse(
            token=refresh_session.token,
            token_type=self.settings.refresh_session.token.type,
            ttl=self.settings.refresh_session.token.expire_in_seconds
        )

    async def validate_refresh_session(self, refresh_token: str) -> RefreshSession:
        refresh_session = await self._delete_refresh_session(refresh_token)
        if refresh_session.is_expired:
            raise RefreshSessionExpiredError
        return refresh_session

    async def _delete_refresh_session(self, refresh_token: str) -> RefreshSession:
        session = await self.refresh_sessions_repo.delete_by_token(refresh_token)
        if session is None:
            raise RefreshSessionDoesNotExistError
        return session
