import logging

from fastapi import (
    Depends,
    HTTPException,
    Security
)
from fastapi.security import HTTPAuthorizationCredentials
from jose import (
    ExpiredSignatureError,
    JWTError
)
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)

from .patched.security import PatchedHTTPBearer
from ..settings import AppSettingsMarker
from ....core.settings import AppSettings
from ....db.errors import EntityDoesNotExistError
from ....db.models import User
from ....db.repos import UsersRepo
from ....resources.strings.authentication import (
    ACCESS_TOKEN_IS_INVALID,
    CURRENT_USER_IN_NOT_ACTIVE,
    CURRENT_USER_IS_NOT_SUPERUSER,
    OWNER_OF_ACCESS_TOKEN_DOES_NOT_EXIST,
    SESSION_EXPIRED
)
from ....services.jwt import JWTService
from ....services.jwt.dataclasses_ import JWTUser


__all__ = [
    'get_current_active_user',
    'get_current_superuser'
]


logger = logging.getLogger(__name__)

patched_http_bearer = PatchedHTTPBearer()


def _get_access_token(
        credentials: HTTPAuthorizationCredentials = Security(patched_http_bearer)
) -> str:
    return credentials.credentials


def _get_jwt_user(
        access_token: str = Depends(_get_access_token),
        settings: AppSettings = Depends(AppSettingsMarker)
) -> JWTUser:
    try:
        jwt_user = JWTService(
            jwt_settings=settings.jwt,
            token_settings=settings.access_token
        ).verify(access_token)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=SESSION_EXPIRED
        )
    except JWTError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=ACCESS_TOKEN_IS_INVALID
        )
    else:
        return jwt_user


async def _get_current_user(
        jwt_user: JWTUser = Depends(_get_jwt_user),
        users_repo: UsersRepo = Depends()
) -> User:
    try:
        current_user = await users_repo.fetch_by_email(jwt_user.email)
    except EntityDoesNotExistError as error:
        logger.exception(
            'Handled access token with nonexistent user.',
            exc_info=error
        )
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=OWNER_OF_ACCESS_TOKEN_DOES_NOT_EXIST
        )
    else:
        return current_user


def get_current_active_user(
        current_user: User = Depends(_get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=CURRENT_USER_IN_NOT_ACTIVE
        )
    return current_user
1

def get_current_superuser(
        current_active_user: User = Depends(get_current_active_user)
) -> User:
    if not current_active_user.is_superuser:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=CURRENT_USER_IS_NOT_SUPERUSER
        )
    return current_active_user
