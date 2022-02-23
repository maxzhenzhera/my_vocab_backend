from fastapi import APIRouter

from .authentication.oauth import router as oauth_router
from .authentication.server import router as server_authentication_router


__all__ = ['router']


router = APIRouter()

router.include_router(
    router=server_authentication_router,
    tags=['Authentication'],
    prefix='/auth'
)
router.include_router(
    router=oauth_router,
    prefix='/oauth'
)
