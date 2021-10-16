import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from starlette.status import HTTP_400_BAD_REQUEST

from ....schemas.authentication import AuthenticationResult
from ....schemas.user import UserInCreate
from ....services.authentication import (
    AuthenticationService,
    CookieService
)
from ....services.authentication.errors import RegistrationError
from ....services.mail import MailService


__all__ = ['router']


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post('/register', response_model=AuthenticationResult, name='auth:register')
async def register(
        user_in_create: UserInCreate,
        authentication_service: AuthenticationService = Depends(),
        cookie_service: CookieService = Depends(),
        mail_service: MailService = Depends()
):
    """
    Register an user with the given credentials.

    Arguments
    ---------
        < UserInCreate > model

    Return
    ---------
        * Body
            < AuthenticationResult > model
        * Cookies
            < refresh_token> httpOnly cookie
    """

    try:
        authentication_result = await authentication_service.register(user_in_create)
    except RegistrationError as error:
        raise HTTPException(HTTP_400_BAD_REQUEST, error.detail)
    else:
        cookie_service.set_refresh_token(authentication_result.tokens.refresh_token)
        mail_service.send_confirmation_mail(authentication_result.user)
        return authentication_result
