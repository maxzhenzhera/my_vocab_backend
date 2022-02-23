from abc import abstractmethod
from typing import Any

from ..base import BaseAuthenticationService


__all__ = ['BaseServerAuthenticationService']


class BaseServerAuthenticationService(BaseAuthenticationService):
    @abstractmethod
    async def refresh(self, *args: Any, **kwargs: Any) -> Any:
        """ Refresh the user`s session. """
