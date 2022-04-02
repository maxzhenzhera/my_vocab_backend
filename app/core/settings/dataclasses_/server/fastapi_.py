from dataclasses import (
    asdict,
    dataclass
)
from typing import Any


__all__ = ['FastAPISettings']


@dataclass
class FastAPISettings:
    title: str
    version: str
    docs_url: str
    redoc_url: str

    @property
    def kwargs(self) -> dict[str, Any]:
        return asdict(self)
