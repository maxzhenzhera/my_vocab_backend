from dataclasses import dataclass

from authlib.integrations.starlette_client import StarletteRemoteApp
from fastapi import Depends

from ..base import BaseAuthorizer
from .....api.dependencies.oauth import GoogleProviderMarker


__all__ = ['GoogleAuthorizer']


@dataclass
class GoogleAuthorizer(BaseAuthorizer):
    oauth_provider: StarletteRemoteApp = Depends(GoogleProviderMarker)
