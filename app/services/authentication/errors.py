"""
AuthenticationError
    +-- UserWithSuchEmailDoesNotExistError
    +-- IncorrectPasswordError
RegistrationError
    +-- EmailIsAlreadyTakenRegistrationError
"""


__all__ = [
    'AuthenticationError',
    'UserWithSuchEmailDoesNotExistError',
    'IncorrectPasswordError',
    'RegistrationError',
    'EmailIsAlreadyTakenRegistrationError'
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
        return f"Given credentials for registration are invalid."


class EmailIsAlreadyTakenRegistrationError(RegistrationError):
    """ Raised on the registration process if the email is already used by the other user. """

    def __init__(self, email: str) -> None:
        self.email = email

    @property
    def detail(self) -> str:
        return f"Email '{self.email}' is busy. Please, use another email!"
