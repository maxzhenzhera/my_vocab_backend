from pydantic import Field

from .mixed import AppSettingsWithLogging
from ..dataclasses_.server import UvicornSettings


__all__ = ['AppDevSettings']


class AppDevSettings(AppSettingsWithLogging):
    uvicorn_reload: bool = Field(False, env='UVICORN_RELOAD')

    @property
    def uvicorn(self) -> UvicornSettings:
        return UvicornSettings(
            reload=self.uvicorn_reload
        )
