import pytest


__all__ = ['RedirectToGoogleOAuthFixturesMixin']


class RedirectToGoogleOAuthFixturesMixin:
    @pytest.fixture(name='redirect_location_domain')
    def fixture_redirect_location_domain(self) -> str:
        return 'google.com'
