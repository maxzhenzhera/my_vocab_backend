from ..base import BaseAuthorizer


__all__ = ['GoogleAuthorizer']


class GoogleAuthorizer(BaseAuthorizer):
    @property
    def oauth_provider_name(self) -> str:
        return self.settings.oauth.google.name
