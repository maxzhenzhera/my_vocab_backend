from dataclasses import dataclass


__all__ = ['OAuthUser']


@dataclass
class OAuthUser:
    id: str
    """ OAuth sub. """
    email: str
