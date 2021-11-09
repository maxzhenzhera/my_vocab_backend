from pydantic import BaseModel


__all__ = [
    'BaseOAuthConnection',
    'GoogleOAuthConnection'
]


class BaseOAuthConnection(BaseModel):
    """
    Must be complemented with OAuth service user id
    with the field name equal to the field name in <db.models.auth.OAuthConnection>.
    """

    user_id: int


class GoogleOAuthConnection(BaseOAuthConnection):
    google_id: str
