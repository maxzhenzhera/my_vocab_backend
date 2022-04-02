from dataclasses import dataclass


__all__ = ['SessionSettings']


@dataclass
class SessionSettings:
    secret: str
