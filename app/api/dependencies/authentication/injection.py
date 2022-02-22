from .authentication import (
    get_current_active_user,
    get_current_superuser
)
from .markers import (
    CurrentSuperuserMarker,
    CurrentUserMarker
)
from ....builder import AppBuilder


__all__ = ['inject_authentication']


def inject_authentication(builder: AppBuilder) -> None:
    builder.app.dependency_overrides[CurrentUserMarker] = get_current_active_user
    builder.app.dependency_overrides[CurrentSuperuserMarker] = get_current_superuser
