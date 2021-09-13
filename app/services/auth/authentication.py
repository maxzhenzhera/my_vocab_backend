import logging
from dataclasses import dataclass

from fastapi import Depends, Request

from .errors import (
    UserWithSuchEmailDoesNotExistError,
    IncorrectPasswordError
)
from .types import RefreshSessionData
from ...api.dependencies.db import get_repository
from ...db.errors import (
    EntityDoesNotExistError,
    EmailIsAlreadyTakenError
)
from ...db.models import (
    User,
    RefreshSession
)
from ...db.repositories import (
    RefreshSessionsRepository,
    UsersRepository
)
from ...schemas.auth import AuthenticationResult
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
    request: Request
    users_repository: UsersRepository = Depends(get_repository(UsersRepository))
    refresh_sessions_repository: RefreshSessionsRepository = Depends(get_repository(RefreshSessionsRepository))

    @property
    def client_ip_address(self) -> str:
        return self.request.client.host

    @property
    def client_user_agent(self) -> str:
        return self.request.headers['user-agent']

    async def register(self, user_in_create: UserInCreate) -> AuthenticationResult:
        if await self.users_repository.check_email_is_taken(user_in_create.email):
            raise EmailIsAlreadyTakenError(user_in_create.email)
        user = UserPasswordService(User(email=user_in_create.email)).change_password(user_in_create.password)
        await self.users_repository.create_by_entity(user)
        return await self._authenticate(user)

    async def login(self, user_in_login: UserInLogin) -> AuthenticationResult:
        try:
            user = await self.users_repository.fetch_by_email(user_in_login.email)
        except EntityDoesNotExistError as error:
            raise UserWithSuchEmailDoesNotExistError from error
        else:
            if not UserPasswordService(user).verify_password(user_in_login.password):
                raise IncorrectPasswordError
            return await self._authenticate(user)

    async def _authenticate(self, user: User) -> AuthenticationResult:
        tokens = UserJWTService(user).generate_tokens()
        await self._create_refresh_session(RefreshSessionData(user, tokens.refresh_token))
        return AuthenticationResult(tokens=tokens, user=user)   # noqa

    async def _create_refresh_session(self, refresh_session_data: RefreshSessionData) -> None:
        await self.refresh_sessions_repository.create_by_entity(
            RefreshSession(
                refresh_token=refresh_session_data.refresh_token.token,
                ip_address=self.client_ip_address,
                user_agent=self.client_user_agent,
                expires_at=refresh_session_data.refresh_token.expires_at,
                user_id=refresh_session_data.user.id
            )
        )
