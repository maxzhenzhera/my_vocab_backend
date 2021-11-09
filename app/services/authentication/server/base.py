from abc import abstractmethod

from ..base import BaseAuthenticationService
from ....schemas.authentication import AuthenticationResult


__all__ = ['BaseServerAuthenticationService']


class BaseServerAuthenticationService(BaseAuthenticationService):
    @abstractmethod
    async def refresh(self, *args, **kwargs) -> AuthenticationResult:
        """ Refresh the user`s session. """
