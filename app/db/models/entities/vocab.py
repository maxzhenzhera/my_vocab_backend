from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    false
)
from sqlalchemy.orm import relationship

from ..base import Base
from ...constants import CASCADE
from ...enums import Language
from ...functions.server_defaults.utcnow import utcnow


__all__ = ['Vocab']


class Vocab(Base):
    """
    `Vocab` - short form of the `vocabulary`.
    """

    __tablename__ = 'vocabs'

    id = Column(BigInteger, primary_key=True)
    title = Column(String(), nullable=False)
    description = Column(String(512))
    language = Column(Enum(Language, name='language'))
    is_favourite = Column(Boolean, server_default=false(), nullable=False)
    created_at = Column(DateTime, server_default=utcnow(), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete=CASCADE), nullable=False)

    user = relationship('User', back_populates='vocabs')
    tags = relationship('VocabTagsAssociation', back_populates='vocab')
    words = relationship('Word', back_populates='vocab', passive_deletes=True)

    def __repr__(self) -> str:
        return (
            f'Vocab(id={self.id!r}, title={self.title!r}, '
            f'language={self.language!r}, user_id={self.user_id!r})'
        )
