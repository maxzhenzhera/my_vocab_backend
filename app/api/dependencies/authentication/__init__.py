from .injection import inject_authentication
from .markers import (
    CurrentSuperuserMarker,
    CurrentUserMarker
)


__all__ = [
    'inject_authentication',
    'CurrentSuperuserMarker',
    'CurrentUserMarker'
]
