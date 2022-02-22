from typing import (
    Any,
    Protocol
)

from sqlalchemy.sql.dml import UpdateBase


__all__ = ['Returnable']


class Returnable(Protocol):
    def returning(self, *args: Any) -> UpdateBase:
        raise NotImplementedError
