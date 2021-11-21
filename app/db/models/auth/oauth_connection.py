from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    String
)
from sqlalchemy.orm import relationship

from ..base import Base
from ...constants import CASCADE


__all__ = ['OAuthConnection']


class OAuthConnection(Base):
    __tablename__ = 'oauth_connections'

    user_id = Column(
        BigInteger,
        ForeignKey('users.id', ondelete=CASCADE),
        primary_key=True, autoincrement=False
    )
    google_id = Column(String(64), unique=True)

    user = relationship('User', back_populates='oauth_connection')

    def __repr__(self) -> str:
        return f'OAuthConnection(user_id={self.user_id!r}, google_id={self.google_id!r})'
