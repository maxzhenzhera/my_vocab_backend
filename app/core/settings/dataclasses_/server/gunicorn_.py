from dataclasses import (
    asdict,
    dataclass
)
from typing import Any


__all__ = ['GunicornSettings']


@dataclass
class GunicornSettings:
    worker_class: str
    workers: int

    @property
    def kwargs(self) -> dict[str, Any]:
        return asdict(self)
