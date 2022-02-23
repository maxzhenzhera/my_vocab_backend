import pytest
from httpx import (
    AsyncClient,
    Response
)

from .annotation import ResponseAndClient
from .protocol import HasResponseAndClientOnSuccessFixture


__all__ = ['ResponseAndClientFixturesMixin']


class ResponseAndClientFixturesMixin:
    @pytest.fixture(name='success_response')
    def fixture_success_response(
            self: HasResponseAndClientOnSuccessFixture,
            response_and_client_on_success: ResponseAndClient
    ) -> Response:
        return response_and_client_on_success[0]

    @pytest.fixture(name='success_client')
    def fixture_success_client(
            self: HasResponseAndClientOnSuccessFixture,
            response_and_client_on_success: ResponseAndClient
    ) -> AsyncClient:
        return response_and_client_on_success[1]
