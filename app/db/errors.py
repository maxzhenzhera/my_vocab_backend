"""
DBError
    +-- EntityDoesNotExistError
    +-- UserUpdateError
        +-- EmailInUpdateIsAlreadyTakenError
"""


__all__ = [
    'DBError',
    'EntityDoesNotExistError',
    'UserUpdateError',
    'EmailInUpdateIsAlreadyTakenError'
]


class DBError(Exception):
    """ Common DB exception. """


class EntityDoesNotExistError(DBError):
    """ Raised if the searched entity does not exist in the database. """


class UserUpdateError(DBError):
    """ Common user update exception. """

    @property
    def detail(self) -> str:
        return 'Given data is invalid for user update.'


class EmailInUpdateIsAlreadyTakenError(UserUpdateError):
    """ Raised on the user update if the email is already used by the other user. """

    def __init__(self, email: str) -> None:
        self.email = email

    @property
    def detail(self) -> str:
        return f"Email '{self.email}' is busy. Please, use another email!"
