import uuid

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    String
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from ..base import Base
from ...functions import utcnow


__all__ = ['User']


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    email = Column(String, nullable=False, index=True, unique=True)
    hashed_password = Column(String, nullable=False)
    password_salt = Column(String, nullable=False)
    activation_link = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_email_confirmed = Column(Boolean, default=False, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=utcnow(), nullable=False)
    email_confirmed_at = Column(DateTime)

    tags = relationship('Tag', back_populates='user')
    vocabs = relationship('Vocab', back_populates='user')
    words = relationship('Word', back_populates='user')
    refresh_sessions = relationship('RefreshSession', back_populates='user')

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, email={self.email!r})'
