from typing import ClassVar

import pytest

from .mixins import RedirectToGoogleOAuthFixturesMixin
from ..base import BaseTestRedirectToOAuthRouteCase


pytestmark = pytest.mark.asyncio


class GoogleSignupRouteNameMixin:
    route_name: ClassVar[str] = 'oauth:google:signup'


class TestGoogleSignupRouteSingleCase(
    GoogleSignupRouteNameMixin,
    RedirectToGoogleOAuthFixturesMixin,
    BaseTestRedirectToOAuthRouteCase
):
    pass
