__all__ = [
    'DBError',
    'EntityDoesNotExistError',
    'EmailIsAlreadyTakenError'
]


class DBError(Exception):
    """ Common DB exception. """


class EntityDoesNotExistError(DBError):
    """ Raised if the searched entity does not exist in the database. """


class EmailIsAlreadyTakenError(DBError):
    """ Raised if the email is already used by the other user. """
    def __init__(self, email: str) -> None:
        self.email = email

    @property
    def detail(self) -> str:
        return f"Email '{self.email}' is busy. Please, use another email!"
