from abc import (
    ABC,
    abstractmethod
)

import pytest
from fastapi import FastAPI
from starlette.datastructures import URLPath


__all__ = ['BaseTestRoute']


class BaseTestRoute(ABC):
    @property
    @abstractmethod
    def route_name(self) -> str:
        """ The name of the testing route. """

    @pytest.fixture(name='route_url')
    def fixture_route_url(self, app: FastAPI) -> URLPath:
        return app.url_path_for(self.route_name)
