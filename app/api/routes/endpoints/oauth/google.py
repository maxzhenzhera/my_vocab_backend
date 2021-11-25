import logging

from authlib.integrations.starlette_client import OAuthError
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

from .....schemas.authentication import AuthenticationResult
from .....services.authentication.cookie import CookieService
from .....services.authentication.errors import (
    AuthenticationError,
    RegistrationError
)
from .....services.authentication.oauth.client import oauth
from .....services.authentication.oauth.google import (
    GoogleAuthorizer,
    GoogleOAuthService
)
from .....services.mail import MailService


__all__ = ['router']


logging = logging.getLogger(__name__)

router = APIRouter()


@router.get('/signup', name='oauth:google:signup')
async def google_signup(request: Request) -> RedirectResponse:
    return await oauth.google.authorize_redirect(request, request.url_for('oauth:google:register'))


@router.get('/signin', name='oauth:google:signin')
async def google_signin(request: Request) -> RedirectResponse:
    return await oauth.google.authorize_redirect(request, request.url_for('oauth:google:login'))


@router.get('/register', response_model=AuthenticationResult, name='oauth:google:register')
async def google_register(
        google_authorizer: GoogleAuthorizer = Depends(),
        google_oauth_service: GoogleOAuthService = Depends(),
        cookie_service: CookieService = Depends(),
        mail_service: MailService = Depends()
) -> AuthenticationResult:
    try:
        google_user = await google_authorizer.get_oauth_user()
    except OAuthError as error:
        raise HTTPException(HTTP_400_BAD_REQUEST, detail=error.error)
    else:
        try:
            oauth_registration_result = await google_oauth_service.register(google_user)
        except RegistrationError as error:
            raise HTTPException(HTTP_400_BAD_REQUEST, error.detail)
        else:
            credentials, authentication_result = (
                oauth_registration_result.credentials,
                oauth_registration_result.authentication_result
            )
            cookie_service.set_refresh_token(authentication_result.refresh_token)
            mail_service.send_credentials_mail(credentials)
            return authentication_result


@router.get('/login', name='oauth:google:login')
async def google_login(
        google_authorizer: GoogleAuthorizer = Depends(),
        google_oauth_service: GoogleOAuthService = Depends(),
        cookie_service: CookieService = Depends()
) -> AuthenticationResult:
    try:
        google_user = await google_authorizer.get_oauth_user()
    except OAuthError as error:
        raise HTTPException(HTTP_400_BAD_REQUEST, detail=error.error)
    else:
        try:
            authentication_result = await google_oauth_service.login(google_user)
        except AuthenticationError as error:
            raise HTTPException(HTTP_401_UNAUTHORIZED, error.detail)
        else:
            cookie_service.set_refresh_token(authentication_result.refresh_token)
            return authentication_result
