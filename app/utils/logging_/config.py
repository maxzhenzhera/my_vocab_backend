import logging
import logging.config
from typing import Any

from .filters import StdoutFilter
from .handlers import TGHandler
from ...core.settings.app import AppSettingsWithLogging


__all__ = [
    'configure_base_logging',
    'get_logging_config'
]


def configure_base_logging() -> None:
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        # Formatters
        # ---------------------------------------
        'formatters': {
            'standard': {
                'style': '{',
                'format': (
                    '[{asctime}] [{process}] [{levelname}] '
                    '{name}: {message}'
                ),
                'datefmt': '%Y-%m-%d %H:%M:%S %z'
            }
        },
        # Filters
        # ---------------------------------------
        'filters': {
            'StdoutFilter': {
                '()': StdoutFilter
            }
        },
        # Handlers
        # ---------------------------------------
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': logging.DEBUG,
                'formatter': 'standard',
                'stream': 'ext://sys.stdout',
                'filters': ['StdoutFilter']
            },
            'error_console': {
                'class': 'logging.StreamHandler',
                'level': logging.WARNING,
                'formatter': 'standard',
                'stream': 'ext://sys.stderr'
            }
        },
        # Root logger
        # ---------------------------------------
        'root': {
            'level': logging.INFO,
            'handlers': [
                'console',
                'error_console'
            ]
        }
    }
    logging.config.dictConfig(config)


def get_logging_config(settings: AppSettingsWithLogging) -> dict[str, Any]:
    return {
        'version': 1,
        'disable_existing_loggers': False,
        # Formatters
        # ---------------------------------------
        'formatters': {
            'standard': {
                'style': '{',
                'format': (
                    '[{asctime}] [{process}] [{levelname}] '
                    '{name}: {message}'
                ),
                'datefmt': '%Y-%m-%d %H:%M:%S %z'
            },
            'detailed': {
                'style': '{',
                'format': (
                    '[{asctime}] [{process}] [{levelname}] '
                    '{name} - {funcName}()[{lineno}]: {message}'
                ),
                'datefmt': '%Y-%m-%d %H:%M:%S %z'
            }
        },
        # Filters
        # ---------------------------------------
        'filters': {
            'StdoutFilter': {
                '()': StdoutFilter
            }
        },
        # Handlers
        # ---------------------------------------
        'handlers': {
            'server_console': {
                'class': 'logging.StreamHandler',
                'level': logging.DEBUG,
                'formatter': 'standard',
                'stream': 'ext://sys.stdout',
                'filters': ['StdoutFilter']
            },
            'server_error_console': {
                'class': 'logging.StreamHandler',
                'level': logging.WARNING,
                'formatter': 'standard',
                'stream': 'ext://sys.stderr'
            },
            'console': {
                'class': 'logging.StreamHandler',
                'level': logging.DEBUG,
                'formatter': 'detailed',
                'stream': 'ext://sys.stdout',
                'filters': ['StdoutFilter']
            },
            'error_console': {
                'class': 'logging.StreamHandler',
                'level': logging.WARNING,
                'formatter': 'detailed',
                'stream': 'ext://sys.stderr'
            },
            'tg_handler': {
                '()': TGHandler,
                'level_': logging.ERROR,
                'settings': settings,
                'formatter': 'detailed'
            }
        },
        # Root logger
        # ---------------------------------------
        'root': {
            'level': settings.logging.level,
            'handlers': [
                'console',
                'error_console',
                'tg_handler'
            ]
        },
        # Loggers
        # ---------------------------------------
        'loggers': {
            'sqlalchemy.engine': {
                'level': logging.INFO,
                'propagate': True
            },
            'gunicorn.access': {
                'level': logging.INFO,
                'handlers': [
                    'server_console',
                    'server_error_console',
                    'tg_handler'
                ],
                'propagate': False
            },
            'gunicorn.error': {
                'level': logging.INFO,
                'handlers': [
                    'server_console',
                    'server_error_console',
                    'tg_handler'
                ],
                'propagate': False
            },
            'uvicorn.access': {
                'level': logging.INFO,
                'handlers': [
                    'server_console',
                    'server_error_console',
                    'tg_handler'
                ],
                "propagate": False
            },
            'uvicorn.error': {
                'level': logging.INFO,
                'handlers': [
                    'server_console',
                    'server_error_console',
                    'tg_handler'
                ],
                'propagate': False
            }
        }
    }
