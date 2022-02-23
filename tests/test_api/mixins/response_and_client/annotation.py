from typing import TypeAlias

from httpx import (
    AsyncClient,
    Response
)


__all__ = ['ResponseAndClient']


ResponseAndClient: TypeAlias = tuple[Response, AsyncClient]
