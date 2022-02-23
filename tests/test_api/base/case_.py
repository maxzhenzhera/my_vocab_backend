from abc import ABC

from .route import BaseTestRoute
from ..mixins import ResponseAndClientFixturesMixin


class BaseTestRouteCase(BaseTestRoute, ResponseAndClientFixturesMixin, ABC):
    """
    Base for route cases testing.

    Route case - successful result variant of the tested route.

    So, this means that for each route case
    that route has
    new test route case have to be written.
    """
