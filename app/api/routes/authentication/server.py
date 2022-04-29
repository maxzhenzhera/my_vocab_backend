import logging
from uuid import UUID

from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    HTTPException,
    Query
)
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED
)

from ....db.errors import EntityDoesNotExistError
from ....db.models import User
from ....db.repos import UsersRepo
from ....resources.strings.authentication import CONFIRMATION_LINK_IS_INVALID
from ....schemas.authentication import AuthenticationResult
from ....schemas.entities.user import (
    UserInCreate,
    UserInLogin,
    UserInResponse
)
from ....schemas.fastapi_ import HTTPExceptionSchema
from ....services.authentication.authenticator import Authenticator
from ....services.authentication.authenticator.cookie import REFRESH_TOKEN_COOKIE_KEY
from ....services.authentication.errors import (
    LoginError,
    RefreshError,
    RefreshSessionDoesNotExistError,
    RegistrationError
)
from ....services.authentication.server import AuthenticationService
from ....services.authentication.user_account import UserAccountService
from ....services.mail import MailService
from ....utils.open_api.cookies import (
    SetRefreshTokenCookieAsOpenAPIHeader,
    UnsetRefreshTokenCookieAsOpenAPIHeader
)


__all__ = ['router']


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    path='/create',
    name='auth:create',
    summary='Create a new user.',
    response_model=UserInResponse,
    responses={
        HTTP_200_OK: {
            'model': UserInResponse,
            'description': 'User has been successfully created.'
        },
        HTTP_400_BAD_REQUEST: {
            'model': HTTPExceptionSchema,
            'description': (
                'The given credentials are invalid '
                'or (most likely) already used before.'
            )
        }
    }
)
async def create(
        user_in_create: UserInCreate,
        user_account_service: UserAccountService = Depends()
) -> User:
    """
    Create a new user.

    Just creates a user in db.
    Mostly aims at the test fixtures or manual testing.
    """

    try:
        user = await user_account_service.register_user(user_in_create)
    except RegistrationError as error:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=error.detail
        )
    else:
        return user


@router.post(
    path='/register',
    name='auth:register',
    summary='Register a new user.',
    response_model=AuthenticationResult,
    responses={
        HTTP_200_OK: {
            'model': AuthenticationResult,
            'description': 'User has been successfully registered.',
            'headers': {
                'Set-Cookie': SetRefreshTokenCookieAsOpenAPIHeader
            }
        },
        HTTP_400_BAD_REQUEST: {
            'model': HTTPExceptionSchema,
            'description': (
                'The given credentials are invalid '
                'or (most likely) already used before.'
            )
        }
    }
)
async def register(
        user_in_create: UserInCreate,
        authentication_service: AuthenticationService = Depends(),
        mail_service: MailService = Depends()
) -> AuthenticationResult:
    """
    Register a new user:
    create a user and login him simultaneously.

    ### Mail

    If user has been successfully registered
    send confirmation mail to the passed email.
    """

    try:
        authentication_result = await authentication_service.register(user_in_create)
    except RegistrationError as error:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=error.detail
        )
    else:
        mail_service.send_confirmation(authentication_result.user)
        return authentication_result


@router.post(
    path='/login',
    name='auth:login',
    summary='Login the user.',
    response_model=AuthenticationResult,
    responses={
        HTTP_200_OK: {
            'model': AuthenticationResult,
            'description': 'User has been successfully logged in.',
            'headers': {
                'Set-Cookie': SetRefreshTokenCookieAsOpenAPIHeader
            }
        },
        HTTP_401_UNAUTHORIZED: {
            'model': HTTPExceptionSchema,
            'description': 'The incorrect credentials.'
        }
    }
)
async def login(
        user_in_login: UserInLogin,
        authentication_service: AuthenticationService = Depends(),
) -> AuthenticationResult:
    """ Login the user. """
    try:
        authentication_result = await authentication_service.login(user_in_login)
    except LoginError as error:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=error.detail
        )
    else:
        return authentication_result


@router.get(
    path='/confirm',
    name='auth:confirm',
    summary='Confirm the user`s email.',
    response_model=UserInResponse,
    responses={
        HTTP_200_OK: {
            'model': UserInResponse,
            'description': 'User has been successfully confirmed.'
        },
        HTTP_400_BAD_REQUEST: {
            'model': HTTPExceptionSchema,
            'description': 'The email confirmation link is invalid.'
        }
    }
)
async def confirm(
        email_confirmation_token: UUID = Query(
            ...,
            alias='token',
            title='Email confirmation token'
        ),
        users_repo: UsersRepo = Depends()
) -> User:
    """ Confirm the user`s email. """

    try:
        user = await users_repo.confirm_by_token(str(email_confirmation_token))
    except EntityDoesNotExistError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=CONFIRMATION_LINK_IS_INVALID
        )
    else:
        return user


@router.get(
    path='/logout',
    name='auth:logout',
    summary='Logout the user.',
    responses={
        HTTP_200_OK: {
            'model': None,
            'description': 'User has been successfully logged out.',
            'headers': {
                'Set-Cookie': UnsetRefreshTokenCookieAsOpenAPIHeader
            }
        },
        HTTP_400_BAD_REQUEST: {
            'model': HTTPExceptionSchema,
            'description': 'The refresh session does not exist.'
        }
    }
)
async def logout(
        refresh_token: UUID = Cookie(
            ...,
            alias=REFRESH_TOKEN_COOKIE_KEY
        ),
        authenticator: Authenticator = Depends()
) -> None:
    """ Logout the user. """

    try:
        await authenticator.deauthenticate(str(refresh_token))
    except RefreshSessionDoesNotExistError as error:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=error.detail
        )


@router.get(
    path='/refresh',
    name='auth:refresh',
    summary='Refresh the user`s session.',
    response_model=AuthenticationResult,
    responses={
        HTTP_200_OK: {
            'model': AuthenticationResult,
            'description': 'The user`s session has been successfully refreshed.',
            'headers': {
                'Set-Cookie': SetRefreshTokenCookieAsOpenAPIHeader
            }
        },
        HTTP_401_UNAUTHORIZED: {
            'model': HTTPExceptionSchema,
            'description': (
                '- The current refresh session has expired;\n'
                '- The refresh session with the given refresh token does not exist.'
            )
        }
    }
)
async def refresh(
        refresh_token: UUID = Cookie(
            ...,
            alias=REFRESH_TOKEN_COOKIE_KEY
        ),
        authentication_service: AuthenticationService = Depends()
) -> AuthenticationResult:
    """ Refresh the user`s session. """

    try:
        authentication_result = await authentication_service.refresh(str(refresh_token))
    except RefreshError as error:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=error.detail
        )
    else:
        return authentication_result
