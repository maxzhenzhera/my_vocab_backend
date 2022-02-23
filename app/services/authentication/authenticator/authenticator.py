import logging
from dataclasses import dataclass
from datetime import datetime

from fastapi import Depends

from .cookie import CookieService
from .request_analyzer import RequestAnalyzer
from ..errors import (
    RefreshSessionDoesNotExistError,
    RefreshSessionExpiredError
)
from ...jwt import JWTService
from ....api.dependencies.settings import AppSettingsMarker
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
    settings: AppSettings = Depends(AppSettingsMarker)
    request_analyzer: RequestAnalyzer = Depends()
    refresh_sessions_repo: RefreshSessionsRepo = Depends()
    cookie_service: CookieService = Depends()

    async def authenticate(self, user: User) -> AuthenticationResult:
        session = await self._create_refresh_session(user)
        self.cookie_service.set_refresh_token(session.token)
        return AuthenticationResult(
            tokens=self._form_tokens(
                user=user,
                session=session
            ),
            user=user
        )

    async def _create_refresh_session(self, user: User) -> RefreshSession:
        return await self.refresh_sessions_repo.create_by_entity(
            RefreshSession(
                user_id=user.id,
                ip_address=self.request_analyzer.client_ip_address,
                user_agent=self.request_analyzer.client_user_agent,
                expires_at=self._compute_expire()
            )
        )

    def _compute_expire(self) -> datetime:
        return datetime.utcnow() + self.settings.refresh_token.expire_timedelta

    def _form_tokens(self, user: User, session: RefreshSession) -> TokensInResponse:
        return TokensInResponse(
            access_token=self._form_access_token(user),
            refresh_token=self._form_refresh_token(session)
        )

    def _form_access_token(self, user: User) -> TokenInResponse:
        return TokenInResponse(
            token=JWTService(
                jwt_settings=self.settings.jwt,
                token_settings=self.settings.access_token
            ).generate(user),
            token_type=self.settings.access_token.type,
            ttl=self.settings.access_token.expire_in_seconds
        )

    def _form_refresh_token(self, session: RefreshSession) -> TokenInResponse:
        return TokenInResponse(
            token=session.token,
            token_type=self.settings.refresh_token.type,
            ttl=self.settings.refresh_token.expire_in_seconds
        )

    async def deauthenticate(self, token: str) -> None:
        await self._pull_refresh_session(token)
        self.cookie_service.delete_refresh_token()

    async def validate_refresh_session(self, token: str) -> RefreshSession:
        session = await self._pull_refresh_session(token)
        if session.is_expired:
            raise RefreshSessionExpiredError
        return session

    async def _pull_refresh_session(self, token: str) -> RefreshSession:
        session = await self.refresh_sessions_repo.delete_by_token(token)
        if session is None:
            raise RefreshSessionDoesNotExistError
        return session
