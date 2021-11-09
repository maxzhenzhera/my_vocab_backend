from fastapi import APIRouter

from .endpoints.authentication import router as authentication_router
from .endpoints.oauth import router as oauth_router


__all__ = ['router']


router = APIRouter()

router.include_router(authentication_router, tags=['auth'], prefix='/auth')
router.include_router(oauth_router, tags=['oauth'], prefix='/oauth')
