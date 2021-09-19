from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String
)
from sqlalchemy.orm import relationship

from ..base import Base
from ...constants import CASCADE
from ...functions import utcnow


__all__ = ['Word']


class Word(Base):
    __tablename__ = 'words'

    id = Column(BigInteger, primary_key=True)
    word = Column(String, nullable=False)
    is_learned = Column(Boolean, default=False)
    is_marked = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=utcnow())
    vocab_id = Column(BigInteger, ForeignKey('vocabs.id', ondelete=CASCADE), nullable=False)

    vocab = relationship('Vocab', back_populates='words')

    def __repr__(self) -> str:
        return f'Word(id={self.id!r}, word={self.word!r}, user_id={self.user_id!r}, vocab_id={self.vocab_id!r})'
