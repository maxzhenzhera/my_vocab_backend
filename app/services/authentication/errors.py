"""
AuthenticationError
    +-- UserWithSuchEmailDoesNotExistError
    +-- IncorrectPasswordError
RegistrationError
    +-- EmailIsAlreadyTakenRegistrationError
RefreshError
    +-- RefreshSessionWithSuchRefreshTokenDoesNotExistError
    +-- RefreshSessionExpiredError
"""


__all__ = [
    'AuthenticationError',
    'UserWithSuchEmailDoesNotExistError',
    'IncorrectPasswordError',
    'RegistrationError',
    'EmailIsAlreadyTakenRegistrationError',
    'RefreshError',
    'RefreshSessionWithSuchRefreshTokenDoesNotExistError',
    'RefreshSessionExpiredError'
]


class AuthenticationError(Exception):
    """ Common authentication exception. """

    @property
    def detail(self) -> str:
        return 'The incorrect credentials.'


class UserWithSuchEmailDoesNotExistError(AuthenticationError):
    """ Raised if the searched user with given email has not been found. """


class IncorrectPasswordError(AuthenticationError):
    """ Raised if the given password has not been verified. """


class RegistrationError(Exception):
    """ Common registration exception. """

    @property
    def detail(self) -> str:
        return 'Given credentials for registration are invalid.'


class EmailIsAlreadyTakenRegistrationError(RegistrationError):
    """ Raised on the registration process if the email is already used by the other user. """

    def __init__(self, email: str) -> None:
        self.email = email

    @property
    def detail(self) -> str:
        return f"Email '{self.email}' is busy. Please, use another email!"


class RefreshError(Exception):
    """ Common refresh exception. """

    @property
    def detail(self) -> str:
        return 'Refresh is impossible.'


class RefreshSessionWithSuchRefreshTokenDoesNotExistError(RefreshError):
    """ Raised if the refresh session with the given refresh token does not exist. """

    @property
    def detail(self) -> str:
        return 'The refresh session with the given refresh token does not exist.'


class RefreshSessionExpiredError(RefreshError):
    """ Raised if the refresh session has expired. """

    @property
    def detail(self) -> str:
        return 'The refresh session has expired. Please, login again!'
