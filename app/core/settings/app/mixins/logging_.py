from pydantic import (
    BaseSettings,
    Field,
    SecretStr
)

from ...dataclasses_.logging_ import (
    LoggingSettings,
    TGLoggingSettings
)


__all__ = ['AppSettingsLoggingMixin']


class AppSettingsLoggingMixin(BaseSettings):
    logging_level: str = Field('INFO', env='LOGGING_LEVEL')
    logging_tg_token: SecretStr = Field(..., env='LOGGING_TG_TOKEN')
    logging_tg_admins: list[str] = Field(..., env='LOGGING_TG_ADMINS')

    @property
    def logging(self) -> LoggingSettings:
        return LoggingSettings(
            level=self.logging_level,
            tg=self._logging_tg
        )

    @property
    def _logging_tg(self) -> TGLoggingSettings:
        return TGLoggingSettings(
            token=self.logging_tg_token.get_secret_value(),
            admins=self.logging_tg_admins
        )
