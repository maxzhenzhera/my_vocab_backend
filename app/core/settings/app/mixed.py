from .base import AppSettings
from .mixins import AppSettingsLoggingMixin


__all__ = ['AppSettingsWithLogging']


class AppSettingsWithLogging(AppSettingsLoggingMixin, AppSettings):
    """ Mixed app and logging settings mostly to simplify type hints. """
