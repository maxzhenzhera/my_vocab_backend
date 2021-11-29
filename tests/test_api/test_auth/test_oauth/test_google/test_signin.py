from typing import ClassVar

import pytest
from starlette.datastructures import URLPath

from app.main import app
from ..base import BaseTestRedirectToOauthRoute


pytestmark = pytest.mark.asyncio


class TestGoogleSigninRoute(BaseTestRedirectToOauthRoute):
    url: ClassVar[URLPath] = app.url_path_for('oauth:google:signin')
    redirect_location_domain: ClassVar[str] = 'google.com'
