from dataclasses import dataclass

from .token import TokenSettings


__all__ = ['TokensSettings']


@dataclass
class TokensSettings:
    access: TokenSettings
    refresh: TokenSettings
