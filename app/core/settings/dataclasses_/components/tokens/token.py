from dataclasses import dataclass
from datetime import timedelta


__all__ = ['TokenSettings']


@dataclass
class TokenSettings:
    type: str
    expire_in_seconds: int

    @property
    def expire_timedelta(self) -> timedelta:
        return timedelta(seconds=self.expire_in_seconds)
