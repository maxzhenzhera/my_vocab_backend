from authlib.integrations.starlette_client import (
    OAuth,
    StarletteOAuth2App
)
from fastapi import Depends

from .markers import (
    GoogleProviderMarker,
    OAuthClientMarker
)
from ....builder import AppBuilder


__all__ = ['inject_oauth']


def inject_oauth(builder: AppBuilder) -> None:
    def depend_on_oauth() -> OAuth:
        return builder.app.state.oauth.client

    def depend_on_google(
            oauth_client: OAuth = Depends(OAuthClientMarker)
    ) -> StarletteOAuth2App:
        return getattr(oauth_client, builder.settings.oauth.google.name)

    builder.app.dependency_overrides[OAuthClientMarker] = depend_on_oauth
    builder.app.dependency_overrides[GoogleProviderMarker] = depend_on_google
