from sqlalchemy import DateTime
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import FunctionElement  # type: ignore[attr-defined]


__all__ = ['utcnow']


class UTCNow(FunctionElement):  # type: ignore[misc]
    """
    Docs:
    https://docs.sqlalchemy.org/en/14/core/compiler.html#utc-timestamp-function
    """

    type = DateTime()


@compiles(UTCNow, 'postgresql')  # type: ignore[misc]
def pg_utcnow(element, compiler, **kw) -> str:  # type: ignore[no-untyped-def]
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


# Classes should be named by CamelCase.
# Functions should be named by snake_case.
# Since class represents `FunctionElement` (also means might be used as a function)
# lowercase alias has been created.
utcnow = UTCNow
