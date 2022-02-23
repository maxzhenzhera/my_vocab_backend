from typing import ClassVar

import pytest

from .mixins import GoogleOAuthFixturesMixin
from ..base import (
    BaseTestCommonErrorsOfOAuthRoute,
    BaseTestOAuthLoginRouteCaseByUserWithOAuth,
    BaseTestOAuthLoginRouteCaseByUserWithoutOAuth
)


pytestmark = pytest.mark.asyncio


class GoogleLoginRouteNameMixin:
    route_name: ClassVar[str] = 'oauth:google:login'


class TestGoogleLoginRouteCaseByUserWithOAuth(
    GoogleLoginRouteNameMixin,
    GoogleOAuthFixturesMixin,
    BaseTestOAuthLoginRouteCaseByUserWithOAuth,
):
    pass


class TestGoogleLoginRouteCaseByUserWithoutOAuth(
    GoogleLoginRouteNameMixin,
    GoogleOAuthFixturesMixin,
    BaseTestOAuthLoginRouteCaseByUserWithoutOAuth
):
    pass


class TestCommonErrorsOfGoogleLoginRoute(
    GoogleLoginRouteNameMixin,
    BaseTestCommonErrorsOfOAuthRoute
):
    pass
