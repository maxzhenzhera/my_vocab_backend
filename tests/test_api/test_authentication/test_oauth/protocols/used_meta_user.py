from typing import (
    Any,
    Protocol
)

import pytest

from ....dataclasses_ import MetaUser


__all__ = ['HasUsedMetaUserFixture']


class HasUsedMetaUserFixture(Protocol):
    @pytest.fixture(name='used_meta_user')
    def fixture_used_meta_user(self, *args: Any) -> MetaUser:
        raise NotImplementedError
