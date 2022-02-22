from typing import Optional


__all__ = ['to_bool']


TRUE_STRINGS = {'true', 't', 'yes', '1'}
FALSE_STRINGS = {'false', 'f', 'no', 'not', '0'}


def to_bool(string: Optional[str]) -> bool:
    if string is None:
        return False
    if string.lower() in TRUE_STRINGS:
        return True
    if string.lower() in FALSE_STRINGS:
        return False
    raise ValueError(
        f'Expected to get the optional string to cast. Got {string!r}.\n'
        f'Possible true values: {TRUE_STRINGS}.\n'
        f'Possible false values: {FALSE_STRINGS}.\n'
    )
