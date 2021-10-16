from .base import ModelWithOrmMode
from .jwt import TokensInResponse
from .user import UserInResponse


__all__ = ['AuthenticationResult']


class AuthenticationResult(ModelWithOrmMode):
    tokens: TokensInResponse
    user: UserInResponse
