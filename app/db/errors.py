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
    """ Raised if the email is already used by the other user (essentially, on update). """
