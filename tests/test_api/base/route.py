from abc import (
    ABC,
    abstractmethod
)

from starlette.datastructures import URLPath

from ..mixins.response_and_client import ResponseAndClientFixturesMixin


__all__ = ['BaseTestRoute']


class BaseTestRoute(ResponseAndClientFixturesMixin, ABC):
    @property
    @abstractmethod
    def url(self) -> URLPath:
        """
        The API route URL.

        Abstract *class* attribute:
            url: ClassVar[URLPath] = app.url_path_for(route-name)
        """
