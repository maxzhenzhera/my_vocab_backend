from dataclasses import dataclass

from .tg import TGLoggingSettings


__all__ = ['LoggingSettings']


@dataclass
class LoggingSettings:
    level: str
    tg: TGLoggingSettings
