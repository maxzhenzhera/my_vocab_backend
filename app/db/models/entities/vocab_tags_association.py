from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey
)
from sqlalchemy.orm import relationship

from ..base import Base
from ...constants import CASCADE


__all__ = ['VocabTagsAssociation']


class VocabTagsAssociation(Base):
    __tablename__ = 'vocab_tags_associations'

    vocab_id = Column(BigInteger, ForeignKey('vocabs.id', ondelete=CASCADE), primary_key=True)
    tag_id = Column(BigInteger, ForeignKey('tags.id', ondelete=CASCADE), primary_key=True)

    vocab = relationship("Vocab", back_populates="tags")
    tag = relationship("Tag", back_populates="vocabs")

    def __repr__(self) -> str:
        return f'VocabTagsAssociation(vocab_id={self.vocab_id!r}, tag_id={self.tag_id!r})'
