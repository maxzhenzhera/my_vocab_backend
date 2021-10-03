from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime


__all__ = ['utcnow']


class utcnow(expression.FunctionElement):       # noqa Class names should use CamelCase convention
    """ docs: https://docs.sqlalchemy.org/en/14/core/compiler.html#utc-timestamp-function """
    type = DateTime()


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"
