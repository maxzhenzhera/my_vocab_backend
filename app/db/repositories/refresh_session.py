from .base import BaseRepository
from ..models import RefreshSession


__all__ = ['RefreshSessionsRepository']


class RefreshSessionsRepository(BaseRepository):
    model = RefreshSession
