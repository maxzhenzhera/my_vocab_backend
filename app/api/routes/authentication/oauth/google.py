import logging

from authlib.integrations.starlette_client import (
    OAuthError,
    StarletteOAuth2App
)
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request
)
from fastapi.responses import RedirectResponse
from starlette.status import (
    HTTP_200_OK,
    HTTP_302_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED
)

from ....dependencies.oauth import GoogleProviderMarker
from .....schemas.authentication import AuthenticationResult
from .....schemas.fastapi_ import HTTPExceptionSchema
from .....services.authentication.errors import (
    LoginError,
    RegistrationError
)
from .....services.authentication.oauth.google import (
    GoogleAuthorizer,
    GoogleOAuthService
)
from .....services.mail import MailService


__all__ = ['router']


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    path='/signup',
    name='oauth:google:signup',
    summary='Redirect to the registration through Google OAuth.',
    response_class=RedirectResponse,
    response_description='Redirected to Google OAuth.',
    status_code=HTTP_302_FOUND
)
async def google_signup(
        request: Request,
        provider: StarletteOAuth2App = Depends(GoogleProviderMarker)
) -> RedirectResponse:
    """ Redirect to the registration through Google OAuth. """
    return await provider.authorize_redirect(  # type: ignore[no-any-return]
        request=request,
        redirect_uri=request.url_for('oauth:google:register')
    )


@router.get(
    path='/signin',
    name='oauth:google:signin',
    summary='Redirect to the login through Google OAuth.',
    response_class=RedirectResponse,
    response_description='Redirected to Google OAuth.',
    status_code=HTTP_302_FOUND
)
async def google_signin(
        request: Request,
        provider: StarletteOAuth2App = Depends(GoogleProviderMarker)
) -> RedirectResponse:
    """ Redirect to the login through Google OAuth. """
    return await provider.authorize_redirect(  # type: ignore[no-any-return]
        request=request,
        redirect_uri=request.url_for('oauth:google:login')
    )


@router.get(
    path='/register',
    name='oauth:google:register',
    summary='Callback for registration through Google OAuth.',
    response_model=AuthenticationResult,
    responses={
        HTTP_200_OK: {
            'model': AuthenticationResult,
            'description': 'Google OAuth user has been successfully registered.'
        },
        HTTP_400_BAD_REQUEST: {
            'model': HTTPExceptionSchema,
            'description': (
                '- Security issue on OAuth request processing;\n'
                '- The given credentials are already used before.'
            )
        }
    }
)
async def google_register(
        authorizer: GoogleAuthorizer = Depends(),
        oauth_service: GoogleOAuthService = Depends(),
        mail_service: MailService = Depends()
) -> AuthenticationResult:
    """
    Register a new user through Google OAuth.

    ### Mail

    If user has been successfully registered
    send credentials mail to the parsed email.
    """

    try:
        google_user = await authorizer.get_oauth_user()
    except OAuthError as error:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=error.error
        )
    else:
        try:
            authentication_result, credentials = await oauth_service.register(google_user)
        except RegistrationError as error:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=error.detail
            )
        else:
            mail_service.send_credentials_mail(credentials)
            return authentication_result


@router.get(
    path='/login',
    name='oauth:google:login',
    summary='Callback for login through Google OAuth.',
    response_model=AuthenticationResult,
    responses={
        HTTP_200_OK: {
            'model': AuthenticationResult,
            'description': 'Google OAuth user has been successfully logged in.'
        },
        HTTP_400_BAD_REQUEST: {
            'model': HTTPExceptionSchema,
            'description': (
                '- Security issue on OAuth request processing;\n'
                '- Such user does not exist.'
            )
        }
    }
)
async def google_login(
        authorizer: GoogleAuthorizer = Depends(),
        oauth_service: GoogleOAuthService = Depends(),
) -> AuthenticationResult:
    """ Login a new user through Google OAuth. """
    try:
        google_user = await authorizer.get_oauth_user()
    except OAuthError as error:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=error.error
        )
    else:
        try:
            authentication_result = await oauth_service.login(google_user)
        except LoginError as error:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail=error.detail
            )
        else:
            return authentication_result
