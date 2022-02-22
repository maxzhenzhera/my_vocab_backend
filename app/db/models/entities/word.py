from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
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


if TYPE_CHECKING:
    from .vocab import Vocab


__all__ = ['Word']


class Word(Base, TimestampMixin):
    __tablename__ = 'words'

    id: Mapped[int] = Column(
        BigInteger,
        primary_key=True
    )
    word: Mapped[str] = Column(
        String(256),
        nullable=False
    )
    is_learned: Mapped[bool] = Column(
        Boolean,
        server_default=false(), nullable=False
    )
    is_marked: Mapped[bool] = Column(
        Boolean,
        server_default=false(), nullable=False
    )
    vocab_id: Mapped[int] = Column(
        ForeignKey('vocabs.id', ondelete=CASCADE),
        nullable=False
    )

    vocab: Mapped['Vocab'] = relationship(
        'Vocab',
        back_populates='words'
    )

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'id={self.id!r}, '
            f'word={self.word!r}, '
            f'vocab_id={self.vocab_id!r}'
            ')'
        )
