import logging
from logging import LogRecord


__all__ = ['StdoutFilter']


STDOUT_LEVEL_RANGE = range(logging.DEBUG, logging.INFO + 1)


class StdoutFilter(logging.Filter):
    def filter(self, record: LogRecord) -> bool:
        return record.levelno in STDOUT_LEVEL_RANGE
