__all__ = [
    'AuthenticationError',
    'UserWithSuchEmailDoesNotExistError',
    'IncorrectPasswordError'
]


class AuthenticationError(Exception):
    """ Common authentication exception. """


class UserWithSuchEmailDoesNotExistError(AuthenticationError):
    """ Raised if the searched user with given email has not been found. """


class IncorrectPasswordError(AuthenticationError):
    """ Raised if the given password has not been verified. """
