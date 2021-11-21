from ...entities.user import UserBaseInCreate


__all__ = ['OAuthUser']


class OAuthUser(UserBaseInCreate):
    """
    Contains:
        1. user id in OAuth service;
        2. base fields for user in create.
    """

    id: str
