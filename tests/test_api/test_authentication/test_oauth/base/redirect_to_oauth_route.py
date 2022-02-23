from abc import (
    ABC,
    abstractmethod
)

import pytest
from httpx import (
    AsyncClient,
    Response
)
from starlette.datastructures import URLPath
from starlette.status import HTTP_302_FOUND

from ....base import BaseTestRouteCase
from ....mixins.response_and_client import ResponseAndClient


__all__ = ['BaseTestRedirectToOAuthRouteCase']


class BaseTestRedirectToOAuthRouteCase(
    BaseTestRouteCase,
    ABC
):
    @pytest.fixture(name='redirect_location_domain')
    @abstractmethod
    def fixture_redirect_location_domain(self) -> str:
        """
        The domain of the OAuth redirect location.

        Presented domain will be tested by checking
        that it is in 'location' header in OAuth redirect.

        E.g. for Google it might be:
            1. accounts.google.com
            2. google.com
            3. google
        So, it does not matter - domain is full or not.
        """

    @pytest.fixture(name='response_and_client_on_success')
    async def fixture_response_and_client_on_success(
            self,
            route_url: URLPath,
            client: AsyncClient
    ) -> ResponseAndClient:
        return (
            await client.get(
                url=route_url,
                allow_redirects=False
            ),
            client
        )

    def test_response_is_redirect(self, success_response: Response):
        assert success_response.status_code == HTTP_302_FOUND

    def test_redirect_location_header(
            self,
            redirect_location_domain: str,
            success_response: Response
    ):
        assert redirect_location_domain in success_response.headers['location']

    def test_setting_session_cookie(self, success_response):
        assert 'session' in success_response.cookies
