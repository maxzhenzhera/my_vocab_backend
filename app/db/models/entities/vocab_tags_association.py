from typing import TYPE_CHECKING

from sqlalchemy import (
    Column,
    ForeignKey
)
from sqlalchemy.orm import (
    Mapped,
    relationship
)

from ..base import Base
from ..mixins import TimestampMixin
from ...constants import CASCADE


if TYPE_CHECKING:
    from .tag import Tag
    from .vocab import Vocab


__all__ = ['VocabTagsAssociation']


class VocabTagsAssociation(Base, TimestampMixin):
    __tablename__ = 'vocab_tags_associations'

    vocab_id: Mapped[int] = Column(
        ForeignKey('vocabs.id', ondelete=CASCADE),
        primary_key=True
    )
    tag_id: Mapped[int] = Column(
        ForeignKey('tags.id', ondelete=CASCADE),
        primary_key=True
    )

    vocab: Mapped['Vocab'] = relationship(
        'Vocab',
        back_populates='tags'
    )
    tag: Mapped['Tag'] = relationship(
        'Tag',
        back_populates='vocabs'
    )

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'vocab_id={self.vocab_id!r}, '
            f'tag_id={self.tag_id!r}'
            ')'
        )
