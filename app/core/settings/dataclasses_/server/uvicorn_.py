from dataclasses import dataclass
from typing import Any


__all__ = ['UvicornSettings']


@dataclass
class UvicornSettings:
    reload: bool

    @property
    def kwargs(self) -> dict[str, Any]:
        return {
            'reload': self.reload
        }
