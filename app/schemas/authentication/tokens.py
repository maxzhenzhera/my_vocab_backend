from pydantic import BaseModel


__all__ = [
    'TokenInResponse',
    'TokensInResponse'
]


class TokenInResponse(BaseModel):
    token: str
    token_type: str
    ttl: int


class TokensInResponse(BaseModel):
    access_token: TokenInResponse
    refresh_token: TokenInResponse
