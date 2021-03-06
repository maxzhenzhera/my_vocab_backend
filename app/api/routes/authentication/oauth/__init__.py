from fastapi import APIRouter

from .google import router as google_router


__all__ = ['router']


router = APIRouter()

router.include_router(
    router=google_router,
    tags=['Google OAuth'],
    prefix='/google'
)
