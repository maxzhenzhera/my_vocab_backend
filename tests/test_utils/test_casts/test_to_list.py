from typing import (
    Type,
    TypeVar
)

import pytest

from app.utils.casts import to_list


T = TypeVar('T', int, str)


@pytest.mark.parametrize(
    ('string', 'part_type', 'result'),
    (
            ('*', str, ['*']),
            ('google.com,github.com', str, ['google.com', 'github.com']),
            ('1', int, [1]),
            ('1,2', int, [1, 2]),
            ('aaa, bbb, ccc', str, ['aaa', 'bbb', 'ccc']),
    )
)
def test_result(string: str, part_type: Type[T], result: list[T]):
    assert to_list(string, part_type) == result
