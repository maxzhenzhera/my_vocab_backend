from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    String
)
from sqlalchemy.orm import relationship

from ..base import Base
from ...constants import CASCADE
from ...functions.server_defaults import utcnow


__all__ = ['Tag']


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(BigInteger, primary_key=True)
    tag = Column(String(64), nullable=False)
    description = Column(String(256))
    created_at = Column(DateTime, server_default=utcnow(), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete=CASCADE), nullable=False)

    user = relationship('User', back_populates='tags')
    vocabs = relationship('VocabTagsAssociation', back_populates='tag')

    def __repr__(self) -> str:
        return f'Tag(id={self.id!r}, user_id={self.user_id!r}, tag={self.tag!r})'
