from authlib.integrations.starlette_client import OAuth

from .markers import OAuthClientMarker
from ....builder import AppBuilder


__all__ = ['inject_oauth']


def inject_oauth(builder: AppBuilder) -> None:
    def depend_on_oauth() -> OAuth:
        return builder.app.state.oauth.client

    builder.app.dependency_overrides[OAuthClientMarker] = depend_on_oauth
