from abc import abstractmethod
from typing import Any, TypeAlias

import pytest
from httpx import (
    AsyncClient,
    Response
)


__all__ = [
    'ResponseAndClient',
    'ResponseAndClientFixturesMixin'
]


ResponseAndClient: TypeAlias = tuple[Response, AsyncClient]


class ResponseAndClientFixturesMixin:
    @pytest.fixture(name='response_and_client_on_success')
    @abstractmethod
    async def fixture_response_and_client_on_success(self, *args: Any):
        """
        Fixture the response and the client
        on success route case.

        Passed response and client will be available
        in corresponded fixtures:
            - success_response
            - success_client
        """

    @pytest.fixture(name='success_response')
    def fixture_success_response(
            self,
            response_and_client_on_success: ResponseAndClient
    ) -> Response:
        return response_and_client_on_success[0]

    @pytest.fixture(name='success_client')
    def fixture_success_client(
            self,
            response_and_client_on_success: ResponseAndClient
    ) -> AsyncClient:
        return response_and_client_on_success[1]
