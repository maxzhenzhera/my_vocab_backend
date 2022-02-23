from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Enum,
    ForeignKey,
    String,
    false
)
from sqlalchemy.orm import (
    Mapped,
    relationship
)

from ..base import Base
from ..mixins import TimestampMixin
from ...constants import CASCADE
from ...enums import Language


if TYPE_CHECKING:
    from .user import User
    from .tag import Tag
    from .word import Word


__all__ = ['Vocab']


class Vocab(Base, TimestampMixin):
    """
    `Vocab` - short form of the `vocabulary`.
    """

    __tablename__ = 'vocabs'

    id: Mapped[int] = Column(
        BigInteger,
        primary_key=True
    )
    title: Mapped[str] = Column(
        String(128),
        nullable=False
    )
    description: Mapped[str | None] = Column(
        String(512)
    )
    language: Mapped[Language] = Column(
        Enum(Language, name='language')
    )
    is_favourite: Mapped[bool] = Column(
        Boolean,
        server_default=false(), nullable=False
    )
    user_id: Mapped[int] = Column(
        ForeignKey('users.id', ondelete=CASCADE),
        nullable=False
    )

    user: Mapped['User'] = relationship(
        'User',
        back_populates='vocabs'
    )
    tags: Mapped[list['Tag']] = relationship(
        'VocabTagsAssociation',
        back_populates='vocab'
    )
    words: Mapped[list['Word']] = relationship(
        'Word',
        back_populates='vocab', passive_deletes=True
    )

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'id={self.id!r}, '
            f'title={self.title!r}, '
            f'language={self.language!r}, '
            f'user_id={self.user_id!r}'
            ')'
        )
