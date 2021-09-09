from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    func
)
from sqlalchemy.orm import relationship

from ..base import Base


__all__ = ['Word']


class Word(Base):
    __tablename__ = 'words'

    id = Column(BigInteger, primary_key=True)
    word = Column(String, nullable=False)
    is_learned = Column(Boolean, default=False)
    is_marked = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    vocab_id = Column(BigInteger, ForeignKey('vocabs.id'), nullable=False)

    user = relationship('User', back_populates='words')
    vocab = relationship('Vocab', back_populates='words')

    def __repr__(self) -> str:
        return f'Word(id={self.id!r}, word={self.word!r}, user_id={self.user_id!r}, vocab_id={self.vocab_id!r})'
