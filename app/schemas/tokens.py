from pydantic import BaseModel


__all__ = ['TokensInResponse']


class TokensInResponse(BaseModel):
    access_token: str
    refresh_token: str
