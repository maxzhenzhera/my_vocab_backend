from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey
)
from sqlalchemy.orm import (
    Mapped,
    declarative_mixin,
    declared_attr,
    relationship
)

from ..entities.user import User
from ...constants import CASCADE


__all__ = ['UserMixin']


@declarative_mixin
class UserMixin:
    @declared_attr
    def user_id(self) -> Column[BigInteger]:
        return Column(
            ForeignKey('users.id', ondelete=CASCADE),
            nullable=False
        )

    @declared_attr
    def user(self) -> Mapped[User]:
        return relationship('User')
