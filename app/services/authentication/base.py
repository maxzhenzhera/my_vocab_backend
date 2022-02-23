from abc import (
    ABC,
    abstractmethod
)
from dataclasses import dataclass
from typing import Any

from fastapi import Depends

from .authenticator import Authenticator
from .user_account import UserAccountService


__all__ = ['BaseAuthenticationService']


@dataclass  # type: ignore[misc]
class BaseAuthenticationService(ABC):
    authenticator: Authenticator = Depends()
    user_account_service: UserAccountService = Depends()

    @abstractmethod
    async def register(self, *args: Any, **kwargs: Any) -> Any:
        """ Register a new user. """

    @abstractmethod
    async def login(self, *args: Any, **kwargs: Any) -> Any:
        """ Login the existed user. """
