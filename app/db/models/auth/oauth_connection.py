from typing import TYPE_CHECKING

from sqlalchemy import (
    Column,
    ForeignKey,
    String
)
from sqlalchemy.orm import (
    Mapped,
    relationship
)

from ..base import Base
from ..mixins import TimestampMixin
from ...constants import CASCADE


if TYPE_CHECKING:
    from ..entities.user import User


__all__ = ['OAuthConnection']


class OAuthConnection(Base, TimestampMixin):
    __tablename__ = 'oauth_connections'

    user_id: Mapped[int] = Column(
        ForeignKey('users.id', ondelete=CASCADE),
        primary_key=True, autoincrement=False
    )
    google_id: Mapped[str | None] = Column(
        String(64),
        unique=True
    )

    user: Mapped['User'] = relationship(
        'User',
        back_populates='oauth_connection'
    )

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'user_id={self.user_id!r}, '
            f'google_id={self.google_id!r}'
            ')'
        )
