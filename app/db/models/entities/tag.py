from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
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
    from .user import User
    from .vocab import Vocab


__all__ = ['Tag']


class Tag(Base, TimestampMixin):
    __tablename__ = 'tags'

    id: Mapped[int] = Column(
        BigInteger,
        primary_key=True
    )
    tag: Mapped[str] = Column(
        String(64),
        nullable=False
    )
    description: Mapped[str | None] = Column(
        String(256)
    )
    user_id: Mapped[int] = Column(
        ForeignKey('users.id', ondelete=CASCADE),
        nullable=False
    )

    user: Mapped['User'] = relationship(
        'User',
        back_populates='tags'
    )

    vocabs: Mapped[list['Vocab']] = relationship(
        'VocabTagsAssociation',
        back_populates='tag'
    )

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'id={self.id!r}, '
            f'user_id={self.user_id!r}, '
            f'tag={self.tag!r}'
            ')'
        )
