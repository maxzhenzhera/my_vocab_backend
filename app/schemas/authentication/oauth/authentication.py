from pydantic import BaseModel

from ..authentication import AuthenticationResult
from ...entities.user import UserInLogin


__all__ = ['OAuthRegistrationResult']


class OAuthRegistrationResult(BaseModel):
    authentication_result: AuthenticationResult
    credentials: UserInLogin
