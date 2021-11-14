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
from sqlalchemy.orm import relationship

from ..base import Base
from ...functions.server_defaults import (
    utcnow,
    gen_random_uuid
)


__all__ = ['User']


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    email = Column(String(256), nullable=False, index=True, unique=True)
    hashed_password = Column(String(128), nullable=False)
    password_salt = Column(String(128), nullable=False)
    email_confirmation_link = Column(UUID, server_default=gen_random_uuid(), nullable=False)
    is_active = Column(Boolean, server_default=true(), nullable=False)
    is_email_confirmed = Column(Boolean, server_default=false(), nullable=False)
    is_superuser = Column(Boolean, server_default=false(), nullable=False)
    created_at = Column(DateTime, server_default=utcnow(), nullable=False)
    email_confirmed_at = Column(DateTime)

    tags = relationship('Tag', back_populates='user', passive_deletes=True)
    vocabs = relationship('Vocab', back_populates='user', passive_deletes=True)
    refresh_sessions = relationship('RefreshSession', back_populates='user', passive_deletes=True)
    oauth_connection = relationship('OAuthConnection', back_populates='user', passive_deletes=True)

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, email={self.email!r})'
