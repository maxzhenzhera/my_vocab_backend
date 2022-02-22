from typing import (
    Any,
    TypeAlias
)

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
    @abstractmethod
    async def fixture_response_and_client_on_success(
            self,
            *args: Any,
            **kwargs: Any
    ) -> ResponseAndClient:
        """
        Abstract fixture that must return the tuple of response and client:

            .. code-block:: python

                return await test_client.get(self.url), test_client_user

        Might be used when different tests of the one test class
        have to have access to *response* and *client* attributes.
        """

    @pytest.fixture(name='success_response')
    def fixture_success_response(
            self,
            response_and_client: ResponseAndClient
    ) -> Response:
        return response_and_client[0]

    @pytest.fixture(name='success_client')
    def fixture_success_client(
            self,
            response_and_client: ResponseAndClient
    ) -> AsyncClient:
        return response_and_client[1]
