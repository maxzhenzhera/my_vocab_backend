from authlib.integrations.starlette_client import (
    OAuth,
    StarletteRemoteApp
)
from fastapi import Depends

from .markers import (
    GoogleProviderMarker,
    OAuthClientMarker
)
from ....builder import AppBuilder
from ....core.settings.constants.oauth import GOOGLE_OAUTH_NAME


__all__ = ['inject_oauth']


def inject_oauth(builder: AppBuilder) -> None:
    def depend_on_oauth() -> OAuth:
        return builder.app.state.oauth.client

    def depend_on_google(
            oauth_client: OAuth = Depends(OAuthClientMarker)
    ) -> StarletteRemoteApp:
        return getattr(oauth_client, GOOGLE_OAUTH_NAME)

    builder.app.dependency_overrides[OAuthClientMarker] = depend_on_oauth
    builder.app.dependency_overrides[GoogleProviderMarker] = depend_on_google
