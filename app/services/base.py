from abc import ABC
from dataclasses import dataclass

from ..db.models import User


__all__ = ['BaseUserService']


@dataclass
class BaseUserService(ABC):
    user: User
