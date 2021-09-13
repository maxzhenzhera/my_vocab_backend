from typing import Optional


__all__ = ['to_bool']


TRUE_STRINGS = {'true', 't', 'yes', '1'}


def to_bool(string: Optional[str]) -> bool:
    return False if not string else string.lower() in TRUE_STRINGS
