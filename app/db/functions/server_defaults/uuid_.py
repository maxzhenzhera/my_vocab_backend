from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression


__all__ = ['uuid_generate_v4']


class uuid_generate_v4(expression.FunctionElement):       # noqa Class names should use CamelCase convention
    type = UUID()


@compiles(uuid_generate_v4, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return 'uuid_generate_v4()'
