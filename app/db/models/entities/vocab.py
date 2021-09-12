from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String
)
from sqlalchemy.orm import relationship

from .. import Base
from ...enums import Language
from ...functions import utcnow


__all__ = ['Vocab']


class Vocab(Base):
    """
    `Vocab` - short form of the `vocabulary`.
    """

    __tablename__ = 'vocabs'

    id = Column(BigInteger, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    language = Column(Enum(Language, name='language'))
    is_favourite = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=utcnow())
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='vocabs')
    tags = relationship('VocabTagsAssociation', back_populates='vocab')
    words = relationship('Word', back_populates='vocab')

    def __repr__(self) -> str:
        return f'Vocab(id={self.id!r}, title={self.title!r}, language={self.language!r}, user_id={self.user_id!r})'
