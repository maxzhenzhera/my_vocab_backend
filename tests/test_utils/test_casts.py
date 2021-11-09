import pytest

from app.utils.casts import to_bool


def test_to_bool():
    assert not to_bool(None)
    assert not to_bool('False')
    assert not to_bool('false')
    assert not to_bool('F')
    assert not to_bool('f')
    assert not to_bool('not')
    assert not to_bool('no')
    assert not to_bool('0')

    assert to_bool('True')
    assert to_bool('true')
    assert to_bool('T')
    assert to_bool('t')
    assert to_bool('yes')
    assert to_bool('1')

    with pytest.raises(ValueError):
        to_bool('')
    with pytest.raises(ValueError):
        to_bool(' ')
    with pytest.raises(ValueError):
        to_bool('Invalid string to cast')
