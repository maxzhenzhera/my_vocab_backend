from typing import ClassVar

import pytest

from .mixins import GoogleOAuthFixturesMixin
from ..base.register import BaseOauthRegisterRouteCase
from ....dataclasses_ import MetaUser


pytestmark = pytest.mark.asyncio


class GoogleSignupRouteNameMixin:
    route_name: ClassVar[str] = 'oauth:google:register'


class TestGoogleRegisterRouteSingleCase(
    GoogleSignupRouteNameMixin,
    GoogleOAuthFixturesMixin,
    BaseOauthRegisterRouteCase
):
    @pytest.fixture(name='used_meta_user')
    def fixture_used_meta_user(self, meta_user_1: MetaUser) -> MetaUser:
        return meta_user_1

    @pytest.fixture(name='created_user_email')
    def fixture_created_user_email(self, used_meta_user: MetaUser) -> str:
        return used_meta_user.email
