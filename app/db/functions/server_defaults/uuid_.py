from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression


__all__ = ['gen_random_uuid']


class gen_random_uuid(expression.FunctionElement):       # noqa Class names should use CamelCase convention
    type = UUID()


@compiles(gen_random_uuid, 'postgresql')
def pg_gen_random_uuid(element, compiler, **kw):
    """ postgres docs: https://www.postgresql.org/docs/14/functions-uuid.html"""
    return 'gen_random_uuid()'
