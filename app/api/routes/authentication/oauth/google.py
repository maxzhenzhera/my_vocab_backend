import logging

from authlib.integrations.starlette_client import (
    OAuth,
    OAuthError
)
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request
)
from fastapi.responses import RedirectResponse
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED
)

from ...dependencies.oauth import OAuthClientMarker
from ....schemas.authentication import AuthenticationResult
from ....services.authentication.errors import (
    LoginError,
    RegistrationError
)
from ....services.authentication.oauth.google import (
    GoogleAuthorizer,
    GoogleOAuthService
)
from ....services.mail import MailService


__all__ = ['router']


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    path='/signup',
    name='oauth:google:signup',
    summary='Redirect to the registration process through Google OAuth.'
)
async def google_signup(
        request: Request,
        oauth_client: OAuth = Depends(OAuthClientMarker)
) -> RedirectResponse:
    return await oauth_client.google.authorize_redirect(
        request=request,
        redirect_uri=request.url_for('oauth:google:register')
    )


@router.get(
    path='/signin',
    name='oauth:google:signin',
    summary='Redirect to the login process through Google OAuth.'
)
async def google_signin(
        request: Request,
        oauth_client: OAuth = Depends(OAuthClientMarker)
) -> RedirectResponse:
    return await oauth_client.google.authorize_redirect(
        request=request,
        redirect_uri=request.url_for('oauth:google:login')
    )


@router.get(
    path='/register',
    name='oauth:google:register',
    summary='Callback for registration through Google OAuth.',
    response_model=AuthenticationResult,
    responses={

    }
)
async def google_register(
        authorizer: GoogleAuthorizer = Depends(),
        oauth_service: GoogleOAuthService = Depends(),
        mail_service: MailService = Depends()
) -> AuthenticationResult:
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

    }
)
async def google_login(
        authorizer: GoogleAuthorizer = Depends(),
        oauth_service: GoogleOAuthService = Depends(),
) -> AuthenticationResult:
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
