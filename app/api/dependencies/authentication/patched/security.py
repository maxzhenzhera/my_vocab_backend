"""
Contains the patched `fastapi.security.http.HTTPBearer`.

Original `fastapi.security.http.HTTPBearer`
raises `HTTP_403_FORBIDDEN` on empty header and not a *bearer* token.

Patched to raise `HTTP_401_UNAUTHORIZED` on such errors.
"""

from fastapi import (
    HTTPException,
    Request
)
from fastapi.openapi.models import HTTPBearer as HTTPBearerModel
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security.http import HTTPBase
from fastapi.security.utils import get_authorization_scheme_param
from starlette.status import HTTP_401_UNAUTHORIZED


__all__ = ['PatchedHTTPBearer']


class PatchedHTTPBearer(HTTPBase):
    def __init__(self) -> None:
        self.model = HTTPBearerModel()
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        authorization: str = request.headers.get('Authorization')
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='Authorization header is invalid.'
            )
        if scheme.lower() != 'bearer':
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='Token is not bearer.',
            )
        return HTTPAuthorizationCredentials(
            scheme=scheme,
            credentials=credentials
        )
