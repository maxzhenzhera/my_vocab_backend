from typing import ClassVar

import pytest

from .mixins import RedirectToGoogleOAuthFixturesMixin
from ..base import BaseTestRedirectToOAuthRouteCase


pytestmark = pytest.mark.asyncio


class GoogleSigninRouteNameMixin:
    route_name: ClassVar[str] = 'oauth:google:signin'


class TestGoogleSigninRouteSingleCase(
    GoogleSigninRouteNameMixin,
    RedirectToGoogleOAuthFixturesMixin,
    BaseTestRedirectToOAuthRouteCase
):
    pass
