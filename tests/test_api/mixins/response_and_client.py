from abc import (
    ABC,
    abstractmethod
)
from typing import TypeVar

import pytest
from httpx import (
    AsyncClient,
    Response
)


__all__ = [
    'ResponseAndClient',
    'ResponseAndClientFixturesMixin'
]


ResponseAndClient = TypeVar('ResponseAndClient', bound=tuple[Response, AsyncClient])


class ResponseAndClientFixturesMixin(ABC):
    @pytest.fixture(name='response_and_client')
    @abstractmethod
    async def fixture_response_and_client(self, *args, **kwargs) -> ResponseAndClient:
        """
        Abstract fixture that must return the tuple of response and client:

            .. code-block:: python

                return await test_client.get(self.url), test_client_user

        Might be used when different tests of the one test class
        have to have access to *response* and *client* attributes.
        """

    @pytest.fixture(name='response')
    def fixture_response(self, response_and_client: ResponseAndClient) -> Response:
        return response_and_client[0]

    @pytest.fixture(name='client')
    def fixture_client(self, response_and_client: ResponseAndClient) -> AsyncClient:
        return response_and_client[1]
