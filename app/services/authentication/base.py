from abc import (
    ABC,
    abstractmethod
)
from dataclasses import dataclass
from typing import TypeVar

from fastapi import Depends
from pydantic import BaseModel

from .refresh_session import RefreshSessionService
from .user_account import UserAccountService


__all__ = ['BaseAuthenticationService']


RegistrationResult = TypeVar('RegistrationResult', bound=BaseModel)
AuthenticationResult = TypeVar('AuthenticationResult', bound=BaseModel)


@dataclass
class BaseAuthenticationService(ABC):
    refresh_session_service: RefreshSessionService = Depends()
    user_account_service: UserAccountService = Depends()

    @abstractmethod
    async def register(self, *args, **kwargs) -> RegistrationResult:
        """ Register a new user. """

    @abstractmethod
    async def login(self, *args, **kwargs) -> AuthenticationResult:
        """ Login the existed user. """
