from abc import abstractmethod

from .route import BaseTestRoute


__all__ = ['BaseTestPostRoute']


class BaseTestPostRoute(BaseTestRoute):
    @property
    @abstractmethod
    def request_json(self) -> dict:
        """
        The API route JSON (sent in request body) for successful response.

        Abstract *class* attribute:
            request_json: ClassVar[dict] = PydanticModel.dict()
        """
