from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    String,
    func
)
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import relationship

from ..base import Base


__all__ = ['RefreshSession']


# //////////////////////////////////////////////
# Template for the future refresh session model
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


class RefreshSession(Base):
    __tablename__ = 'refresh_sessions'

    id = Column(BigInteger, primary_key=True)
    refresh_token = Column(String, nullable=False)
    ip_address = Column(INET, nullable=False)
    user_agent = Column(String, nullable=False)
    fingerprint = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    expires_at = Column(DateTime, nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='refresh_sessions')

    def __repr__(self) -> str:
        return f'RefreshSession(id = {self.id!r}, refresh_token={self.refresh_token!r}, user_id = {self.user_id!r})'
