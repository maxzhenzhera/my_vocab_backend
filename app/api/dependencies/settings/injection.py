from .markers import AppSettingsMarker
from ....builder import AppBuilder
from ....core.settings import AppSettings


__all__ = ['inject_settings']


def inject_settings(builder: AppBuilder) -> None:
    def depend_on_settings() -> AppSettings:
        return builder.settings

    builder.app.dependency_overrides[AppSettingsMarker] = depend_on_settings
