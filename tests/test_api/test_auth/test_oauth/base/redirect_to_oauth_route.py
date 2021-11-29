from abc import (
    ABC,
    abstractmethod
)

import pytest
from httpx import (
    AsyncClient,
    Response
)
from starlette.status import HTTP_302_FOUND

from ....base import BaseTestRoute
from ....mixins.response_and_client import ResponseAndClient


__all__ = ['BaseTestRedirectToOauthRoute']


class BaseTestRedirectToOauthRoute(BaseTestRoute, ABC):
    @property
    @abstractmethod
    def redirect_location_domain(self) -> str:
        """
        The domain of the oauth redirect location.

        Presented domain will be tested by checking
        that it is in 'location' header in oauth redirect.

        E.g. for google it might be:
            1. accounts.google.com
            2. google.com
            3. google
        So, it does not matter - domain is full or not.

        Abstract *class* attribute:
            redirect_location_domain: ClassVar[str] = 'oauth-service.com'
        """

    @pytest.fixture(name='response_and_client')
    async def fixture_response_and_client(self, test_client: AsyncClient) -> ResponseAndClient:
        return await test_client.get(self.url, allow_redirects=False), test_client

    def test_response_is_redirect(self, response: Response):        # noqa Method may be 'static'
        assert response.status_code == HTTP_302_FOUND

    def test_redirect_location_header(self, response: Response):
        assert self.redirect_location_domain in response.headers['location']

    def test_setting_session_cookie(self, response):        # noqa Method may be 'static'
        assert 'session' in response.cookies
