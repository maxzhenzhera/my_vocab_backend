import logging
from typing import Union


__all__ = ['LevelFilter']


class LevelFilter(logging.Filter):
    """ Filters log records by level (includes logs only by one level). """

    def __init__(self, level: Union[int, str]):
        super().__init__()

        if isinstance(level, str):
            self.level: int = getattr(logging, level.upper())
        elif isinstance(level, int):
            self.level: int = level
        else:
            raise ValueError(
                'Expected to get either levelno [int] either levelname [str]. '
                f'Instead got {level!r}.'
            )

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno == self.level
