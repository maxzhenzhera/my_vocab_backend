from fastapi import APIRouter

from .authentication import router as authentication_router


__all__ = ['router']


router = APIRouter()

router.include_router(authentication_router, tags=['auth'], prefix='/auth')
