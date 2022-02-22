from dataclasses import dataclass
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
        return {
            'title': self.title,
            'version': self.version,
            'docs_url': self.docs_url,
            'redoc_url': self.redoc_url
        }
