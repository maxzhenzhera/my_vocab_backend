from typing import ClassVar

import pytest
from starlette.datastructures import URLPath

from app.__main__ import app
from ..base import BaseTestRedirectToOauthRoute


pytestmark = pytest.mark.asyncio


class TestGoogleSignupRoute(BaseTestRedirectToOauthRoute):
    url: ClassVar[URLPath] = app.url_path_for('oauth:google:signup')
    redirect_location_domain: ClassVar[str] = 'google.com'
