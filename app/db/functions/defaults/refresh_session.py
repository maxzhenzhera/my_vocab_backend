from datetime import datetime

from ....core.config import refresh_session_config


__all__ = ['compute_refresh_session_expire']


def compute_refresh_session_expire() -> datetime:
    return datetime.utcnow() + refresh_session_config.REFRESH_TOKEN_EXPIRE_TIMEDELTA
