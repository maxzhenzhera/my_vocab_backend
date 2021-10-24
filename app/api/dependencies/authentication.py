import logging

from fastapi import (
    Security,
    Depends,
    HTTPException
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)
from jose import (
    ExpiredSignatureError,
    JWTError
)
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN
)

from .db import get_repository
from ...db.errors import EntityDoesNotExistError
from ...db.models import User
from ...db.repositories import UsersRepository
from ...schemas.jwt import JWTUser
from ...services.jwt import UserJWTService


__all__ = [
    'get_current_active_user',
    'get_current_superuser'
]


logger = logging.getLogger(__name__)


def _get_access_token(credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())) -> str:
    return credentials.credentials


def _get_jwt_user(access_token: str = Depends(_get_access_token)) -> JWTUser:
    try:
        jwt_user = UserJWTService.verify_access_token(access_token)
    except ExpiredSignatureError:
        raise HTTPException(HTTP_401_UNAUTHORIZED, 'The current session has expired. Please, refresh.')
    except JWTError:
        raise HTTPException(HTTP_401_UNAUTHORIZED, 'Access token is invalid.')
    else:
        return jwt_user


async def _get_current_user(
    jwt_user: JWTUser = Depends(_get_jwt_user),
    users_repository: UsersRepository = Depends(get_repository(UsersRepository))
) -> User:
    try:
        current_user = await users_repository.fetch_by_email(jwt_user.email)
    except EntityDoesNotExistError as error:
        logger.exception('Handled access token with nonexistent user.', exc_info=error)
    else:
        return current_user


def get_current_active_user(current_user: User = Depends(_get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(HTTP_403_FORBIDDEN, 'Current user is not active.')
    return current_user


def get_current_superuser(current_active_user: User = Depends(get_current_active_user)) -> User:
    if not current_active_user.is_superuser:
        raise HTTPException(HTTP_403_FORBIDDEN, 'Current user is not a superuser.')
    return current_active_user
