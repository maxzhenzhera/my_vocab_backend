import logging


__all__ = ['logger']


DEFAULT_LOGGING_CONFIG = {
    "format": (
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s() "
        "[%(lineno)s] : %(message)s"
    ),
    "level": logging.INFO
}


logging.basicConfig(**DEFAULT_LOGGING_CONFIG)
logger = logging.getLogger('scripts')
