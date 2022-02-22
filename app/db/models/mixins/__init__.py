"""
https://docs.sqlalchemy.org/en/14/orm/declarative_mixins.html#mixing-in-columns
https://docs.sqlalchemy.org/en/14/orm/declarative_mixins.html#mixing-in-relationships
https://docs.sqlalchemy.org/en/14/orm/extensions/mypy.html#using-declared-attr-and-declarative-mixins

https://stackoverflow.com/a/4013184/17221540
"""

from .id_ import IDMixin
from .timestamp import TimestampMixin
from .user import UserMixin


__all__ = [
    'IDMixin',
    'TimestampMixin',
    'UserMixin'
]
