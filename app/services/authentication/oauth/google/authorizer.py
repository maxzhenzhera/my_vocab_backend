from typing import ClassVar

from ..base.authorizer import BaseAuthorizer
from ..client import GOOGLE_OAUTH_NAME


__all__ = ['GoogleAuthorizer']


class GoogleAuthorizer(BaseAuthorizer):
    oauth_service_name: ClassVar[str] = GOOGLE_OAUTH_NAME
