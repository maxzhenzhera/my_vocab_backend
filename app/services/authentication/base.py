from abc import (
    ABC,
    abstractmethod
)
from dataclasses import dataclass

from fastapi import Depends

from .authenticator import Authenticator
from ...db.repos import UsersRepo
from ...schemas.auth import AuthenticationResult


__all__ = ['BaseAuthenticationService']


@dataclass
class BaseAuthenticationService(ABC):
    authenticator: Authenticator = Depends()
    users_repo: UsersRepo = Depends()

    @abstractmethod
    async def register(self, *args, **kwargs) -> AuthenticationResult:
        """ Register a new user. """

    @abstractmethod
    async def login(self, *args, **kwargs) -> AuthenticationResult:
        """ Login the existed user. """
