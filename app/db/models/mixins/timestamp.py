from sqlalchemy import (
    Column,
    DateTime
)
from sqlalchemy.orm import (
    declared_attr,
    declarative_mixin
)

from ...functions.server_defaults import utcnow


__all__ = ['TimestampMixin']


@declarative_mixin
class TimestampMixin:
    @declared_attr
    def created_at(self) -> Column[DateTime]:
        return Column(
            DateTime,
            server_default=utcnow(), nullable=False
        )

    @declared_attr
    def updated_at(self) -> Column[DateTime]:
        return Column(
            DateTime,
            server_default=utcnow(), onupdate=utcnow(), nullable=False
        )
