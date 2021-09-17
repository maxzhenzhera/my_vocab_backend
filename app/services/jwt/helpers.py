from jose import jwt
from jose.jwt import (
    JWTError,
    ExpiredSignatureError
)

from .errors import (
    InvalidTokenSignatureError,
    ExpiredTokenSignatureError
)
from .types import TokenDataForDecoding
from ...core.config import jwt_config


__all__ = ['decode_token']


def decode_token(token_data: TokenDataForDecoding) -> dict:
    try:
        payload = jwt.decode(token_data.token, token_data.secret, jwt_config.ALGORITHM)
    except ExpiredSignatureError as error:
        raise ExpiredTokenSignatureError from error
    except JWTError as error:
        raise InvalidTokenSignatureError from error
    else:
        return payload
