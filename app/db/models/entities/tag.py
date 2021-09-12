from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    String
)
from sqlalchemy.orm import relationship

from ..base import Base
from ...functions import utcnow


__all__ = ['Tag']


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(BigInteger, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=utcnow())
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='tags')
    vocabs = relationship('VocabTagsAssociation', back_populates='tag')

    def __repr__(self) -> str:
        return f'Tag(id={self.id!r}, user_id={self.user_id!r}, title={self.title!r})'
