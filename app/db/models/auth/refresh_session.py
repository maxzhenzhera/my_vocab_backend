from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String
)
from sqlalchemy.dialects.postgresql import (
    INET,
    UUID
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import (
    Mapped,
    relationship
)

from ..base import Base
from ..mixins import TimestampMixin
from ...constants import CASCADE
from ...functions.server_defaults import gen_random_uuid


if TYPE_CHECKING:
    from ..entities.user import User


__all__ = ['RefreshSession']


class RefreshSession(Base, TimestampMixin):
    __tablename__ = 'refresh_sessions'

    token: Mapped[str] = Column(
        UUID,
        primary_key=True, server_default=gen_random_uuid()
    )
    ip_address: Mapped[str] = Column(
        INET,
        nullable=False
    )
    user_agent: Mapped[str] = Column(
        String(256),
        nullable=False
    )
    expires_at: Mapped[datetime] = Column(
        DateTime,
        nullable=False
    )
    user_id: Mapped[int] = Column(
        ForeignKey('users.id', ondelete=CASCADE),
        nullable=False
    )

    user: Mapped['User'] = relationship(
        'User',
        back_populates='refresh_sessions'
    )

    @hybrid_property
    def is_expired(self) -> bool:
        return self.expires_at < datetime.utcnow()

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'token={self.token!r}, '
            f'user_id ={self.user_id!r}'
            ')'
        )
