from datetime import (
    datetime,
    timedelta
)


__all__ = ['assert_datetime']


def assert_datetime(
        *,
        expected: datetime | None = None,
        actual: datetime,
        delta: timedelta
) -> None:
    expected = expected or datetime.utcnow()

    if expected > actual:
        assert (expected - actual) < delta
    elif expected < actual:
        assert (actual - expected) < delta
    else:
        assert expected == actual
