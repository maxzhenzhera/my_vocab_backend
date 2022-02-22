from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import FunctionElement  # type: ignore[attr-defined]


__all__ = ['gen_random_uuid']


class GenRandomUUID(FunctionElement):  # type: ignore[misc]
    type = UUID()


@compiles(GenRandomUUID, 'postgresql')  # type: ignore[misc]
def pg_gen_random_uuid(element, compiler, **kw) -> str:  # type: ignore[no-untyped-def]
    """
    Postgres docs:
    https://www.postgresql.org/docs/14/functions-uuid.html
    """

    return 'gen_random_uuid()'


# Classes should be named by CamelCase.
# Functions should be named by snake_case.
# Since class represents `FunctionElement` (also means might be used as a function)
# lowercase alias has been created.
gen_random_uuid = GenRandomUUID
