from dataclasses import dataclass


__all__ = ['OAuthProviderSettings']


@dataclass
class OAuthProviderSettings:
    name: str
    server_metadata_url: str
    client_kwargs: dict[str, str]
    client_id: str
    client_secret: str
