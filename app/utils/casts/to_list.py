from typing import (
    Type,
    TypeVar
)


__all__ = ['to_list']


T = TypeVar('T', int, str)


def to_list(string: str, part_type: Type[T]) -> list[T]:
    return [part_type(part.strip()) for part in string.split(',')]
