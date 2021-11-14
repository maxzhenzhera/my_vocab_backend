from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    String
)
from sqlalchemy.dialects.postgresql import (
    INET,
    UUID
)
from sqlalchemy.orm import relationship

from ..base import Base
from ...constants import CASCADE
from ...functions.defaults.refresh_session import compute_refresh_session_expire
from ...functions.server_defaults import (
    utcnow,
    gen_random_uuid
)


__all__ = ['RefreshSession']


class RefreshSession(Base):
    __tablename__ = 'refresh_sessions'

    refresh_token = Column(UUID, primary_key=True, server_default=gen_random_uuid())
    ip_address = Column(INET, nullable=False)
    user_agent = Column(String(256), nullable=False)
    created_at = Column(DateTime, server_default=utcnow(), nullable=False)
    expires_at = Column(DateTime, default=compute_refresh_session_expire, nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete=CASCADE), nullable=False)

    user = relationship('User', back_populates='refresh_sessions')

    def __repr__(self) -> str:
        return f'RefreshSession(refresh_token={self.refresh_token!r}, user_id ={self.user_id!r})'
