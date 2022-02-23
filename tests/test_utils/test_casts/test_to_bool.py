from typing import Type

import pytest

from app.utils.casts import to_bool


@pytest.mark.parametrize(
    ('string, result'),
    (
            # False
            (None, False),
            ('False', False),
            ('false', False),
            ('F', False),
            ('f', False),
            ('not', False),
            ('no', False),
            ('0', False),
            # True
            ('True', True),
            ('true', True),
            ('T', True),
            ('t', True),
            ('yes', True),
            ('1', True)
    )
)
def test_result(string: str | None, result: bool):
    assert to_bool(string) == result


@pytest.mark.parametrize(
    ('string', 'exception_type'),
    (
            ('', ValueError),
            (' ', ValueError),
            ('Invalid string to cast', ValueError)
    )
)
def test_error(string: str | None, exception_type: Type[Exception]):
    with pytest.raises(exception_type):
        to_bool(string)
