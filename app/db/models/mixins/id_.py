from sqlalchemy import (
    BigInteger,
    Column
)
from sqlalchemy.orm import declarative_mixin


__all__ = ['IDMixin']


@declarative_mixin
class IDMixin:
    id = Column(
        BigInteger,
        primary_key=True
    )
