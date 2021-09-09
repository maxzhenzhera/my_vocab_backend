import logging

from fastapi import APIRouter


__all__ = ['router']


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/test')
async def test_endpoint():
    return 1
