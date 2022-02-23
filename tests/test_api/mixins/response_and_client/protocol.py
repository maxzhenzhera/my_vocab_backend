from typing import (
    Any,
    Protocol
)

import pytest


__all__ = ['HasResponseAndClientOnSuccessFixture']


class HasResponseAndClientOnSuccessFixture(Protocol):
    @pytest.fixture(name='response_and_client_on_success')
    async def fixture_response_and_client_on_success(self, *args: Any):
        raise NotImplementedError
