from .tokens import TokensInResponse
from ..base import ModelWithOrmMode
from ..entities.user import UserInResponse


__all__ = ['AuthenticationResult']


class AuthenticationResult(ModelWithOrmMode):
    tokens: TokensInResponse
    user: UserInResponse

    @property
    def refresh_token(self) -> str:
        return self.tokens.refresh_token.token
