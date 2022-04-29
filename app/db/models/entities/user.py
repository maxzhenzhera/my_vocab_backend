from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    String,
    false,
    true
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    relationship
)

from ..base import Base
from ..mixins import TimestampMixin
from ...functions.server_defaults import gen_random_uuid


if TYPE_CHECKING:
    from .tag import Tag
    from .vocab import Vocab
    from ..auth import (
        OAuthConnection,
        RefreshSession
    )


__all__ = ['User']


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id: Mapped[int] = Column(
        BigInteger,
        primary_key=True
    )
    email: Mapped[str] = Column(
        String(256),
        nullable=False, index=True, unique=True
    )
    hashed_password: Mapped[str] = Column(
        String(128),
        nullable=False
    )
    email_confirmation_token: Mapped[str] = Column(
        UUID,
        server_default=gen_random_uuid(), nullable=False
    )
    is_active: Mapped[bool] = Column(
        Boolean,
        server_default=true(), nullable=False
    )
    is_email_confirmed: Mapped[bool] = Column(
        Boolean,
        server_default=false(), nullable=False
    )
    is_superuser: Mapped[bool] = Column(
        Boolean,
        server_default=false(), nullable=False
    )
    email_confirmed_at: Mapped[datetime | None] = Column(
        DateTime
    )

    tags: Mapped[list['Tag']] = relationship(
        'Tag',
        back_populates='user', passive_deletes=True
    )
    vocabs: Mapped[list['Vocab']] = relationship(
        'Vocab',
        back_populates='user', passive_deletes=True
    )
    refresh_sessions: Mapped[list['RefreshSession']] = relationship(
        'RefreshSession',
        back_populates='user', passive_deletes=True
    )
    oauth_connection: Mapped['OAuthConnection'] = relationship(
        'OAuthConnection',
        back_populates='user', passive_deletes=True
    )

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'id={self.id!r}, '
            f'email={self.email!r}'
            ')'
        )
