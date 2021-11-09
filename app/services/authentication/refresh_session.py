import logging
from dataclasses import dataclass
from datetime import datetime

from fastapi import Depends

from .errors import (
    RefreshSessionDoesNotExistError,
    RefreshSessionExpiredError
)
from .request_analyzer import RequestAnalyzer
from ..jwt import UserJWTService
from ...api.dependencies.db import get_repository
from ...db.models import (
    User,
    RefreshSession
)
from ...db.repositories import RefreshSessionsRepository
from ...schemas.authentication import (
    AuthenticationResult,
    TokensInResponse,
    AccessTokenInResponse,
    RefreshTokenInResponse
)


__all__ = ['RefreshSessionService']


logger = logging.getLogger(__name__)


@dataclass
class RefreshSessionService:
    request_analyzer: RequestAnalyzer = Depends()
    refresh_sessions_repository: RefreshSessionsRepository = Depends(get_repository(RefreshSessionsRepository))

    async def authenticate(self, user: User) -> AuthenticationResult:
        refresh_session = await self._create_refresh_session(user)
        return AuthenticationResult(
            tokens=TokensInResponse(
                access_token=AccessTokenInResponse(token=UserJWTService(user).generate_access_token()),
                refresh_token=RefreshTokenInResponse(token=refresh_session.refresh_token)
            ),
            user=user
        )

    async def _create_refresh_session(self, user: User) -> RefreshSession:
        return await self.refresh_sessions_repository.create_by_entity(
            RefreshSession(
                ip_address=self.request_analyzer.client_ip_address,
                user_agent=self.request_analyzer.client_user_agent,
                user_id=user.id
            )
        )

    async def validate_refresh_session(self, refresh_token: str) -> RefreshSession:
        refresh_session = await self._delete_refresh_session_or_raise_refresh_error(refresh_token)
        if self._check_refresh_session_is_expired(refresh_session):
            raise RefreshSessionExpiredError
        return refresh_session

    async def _delete_refresh_session_or_raise_refresh_error(self, refresh_token: str) -> RefreshSession:
        refresh_session = await self.refresh_sessions_repository.delete_by_refresh_token(refresh_token)
        if refresh_session is None:
            raise RefreshSessionDoesNotExistError
        return refresh_session

    @staticmethod
    def _check_refresh_session_is_expired(refresh_session: RefreshSession) -> bool:
        return refresh_session.expires_at < datetime.utcnow()
