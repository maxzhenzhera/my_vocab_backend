from .injection import inject_oauth
from .markers import (
    GoogleProviderMarker,
    OAuthClientMarker
)


__all__ = [
    'inject_oauth',
    'GoogleProviderMarker',
    'OAuthClientMarker'
]
