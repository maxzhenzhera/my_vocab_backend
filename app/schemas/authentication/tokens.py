from pydantic import BaseModel

from ...core.settings.dataclasses_.components.tokens import TokenSettings


__all__ = [
    'TokenInResponse',
    'TokensInResponse'
]


class TokenInResponse(BaseModel):
    token: str
    token_type: str
    ttl: int

    @classmethod
    def from_settings(cls,  token: str, settings: TokenSettings) -> 'TokenInResponse':
        return cls(
            token=token,
            token_type=settings.type,
            ttl=settings.expire_in_seconds
        )


class TokensInResponse(BaseModel):
    access_token: TokenInResponse
    refresh_token: TokenInResponse
