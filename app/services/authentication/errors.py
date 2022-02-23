"""
AuthenticationError
    +-- LoginError
        +-- UserWithSuchEmailDoesNotExistError
        +-- ServerLoginError
            +-- IncorrectPasswordError
        +-- OAuthLoginError
            +-- OAuthConnectionDoesNotExistError
    +-- RegistrationError
        +-- EmailIsAlreadyTakenError
    +-- RefreshError
        +-- RefreshSessionDoesNotExistError
        +-- RefreshSessionExpiredError
"""

from dataclasses import dataclass
from typing import ClassVar

from ...resources.strings.authentication import (
    EMAIL_IS_ALREADY_TAKEN,
    LOGIN_FAILED,
    REFRESH_SESSION_DOES_NOT_EXIST,
    REFRESH_SESSION_EXPIRED
)


__all__ = [
    'AuthenticationError',
    'LoginError',
    'UserWithSuchEmailDoesNotExistError',
    'ServerLoginError',
    'IncorrectPasswordError',
    'OAuthLoginError',
    'OAuthConnectionDoesNotExistError',
    'RegistrationError',
    'EmailIsAlreadyTakenError',
    'RefreshError',
    'RefreshSessionDoesNotExistError',
    'RefreshSessionExpiredError'
]


class AuthenticationError(Exception):
    """ Common authentication exception. """

    detail: ClassVar[str] = 'Authentication error.'


class LoginError(AuthenticationError):
    """ Common login exception. """

    detail: ClassVar[str] = LOGIN_FAILED


class UserWithSuchEmailDoesNotExistError(LoginError):
    """
    Raised on login process
    if the searched user with the given email has not been found.
    """


class ServerLoginError(LoginError):
    """ Common server login exception. """


class IncorrectPasswordError(ServerLoginError):
    """
    Raised on login (app auth service) process
    if the given password has not been verified.
    """


class OAuthLoginError(LoginError):
    """ Common OAuth login exception. """


class OAuthConnectionDoesNotExistError(OAuthLoginError):
    """
    Raised on OAuth login process
    if the OAuth connection does not exist.
    """


class RegistrationError(AuthenticationError):
    """ Common registration exception. """

    detail: ClassVar[str] = 'Registration error.'


@dataclass
class EmailIsAlreadyTakenError(RegistrationError):
    """
    Raised on the registration process
    if the email is already used by the other user.
    """

    email: str

    @property
    def detail(self) -> str:  # type: ignore[override]
        return EMAIL_IS_ALREADY_TAKEN.format(email=self.email)


class RefreshError(AuthenticationError):
    """ Common refresh exception. """

    detail: ClassVar[str] = 'Refresh error.'


class RefreshSessionDoesNotExistError(RefreshError):
    """
    Raised on refresh (app auth service) process
    if the refresh session with the given refresh token does not exist.
    """

    detail: ClassVar[str] = REFRESH_SESSION_DOES_NOT_EXIST


class RefreshSessionExpiredError(RefreshError):
    """
    Raised on refresh (app auth service) process
    if the refresh session has expired.
    """

    detail: ClassVar[str] = REFRESH_SESSION_EXPIRED
