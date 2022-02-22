from dataclasses import (
    dataclass,
    fields
)

from .provider import OAuthProviderSettings


__all__ = ['OAuthSettings']


@dataclass
class OAuthSettings:
    google: OAuthProviderSettings

    @property
    def providers(self) -> list[OAuthProviderSettings]:
        return [getattr(self, provider.name) for provider in fields(self)]
