import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from starlette.status import HTTP_400_BAD_REQUEST

from ...db.errors import EmailIsAlreadyTakenError
from ...schemas.auth import AuthenticationResult
from ...schemas.user import UserInCreate
from ...services.auth import (
    AuthenticationService,
    CookieService
)
from ...services.mail import MailService


__all__ = ['router']


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post('/register', response_model=AuthenticationResult, name='auth:register')
async def register(
        user_in_create: UserInCreate,
        auth_service: AuthenticationService = Depends(),
        cookie_service: CookieService = Depends(),
        mail_service: MailService = Depends()
):
    try:
        authentication_result = await auth_service.register(user_in_create)
    except EmailIsAlreadyTakenError as error:
        raise HTTPException(HTTP_400_BAD_REQUEST, error.detail)
    else:
        cookie_service.set_refresh_token(authentication_result.tokens.refresh_token)
        mail_service.send_confirmation_mail(authentication_result.user)
        return authentication_result
