from dataclasses import dataclass


__all__ = ['PasswordSettings']


@dataclass
class PasswordSettings:
    pepper: str
