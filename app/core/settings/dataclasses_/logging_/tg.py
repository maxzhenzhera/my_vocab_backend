from dataclasses import dataclass


__all__ = ['TGLoggingSettings']


@dataclass
class TGLoggingSettings:
    token: str
    admins: list[str]
