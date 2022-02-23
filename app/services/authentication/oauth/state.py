import logging
from dataclasses import (
    asdict,
    dataclass
)

from authlib.integrations.starlette_client import OAuth

from ....core.settings.dataclasses_.components import OAuthSettings


__all__ = ['OAuthState']


logger = logging.getLogger(__name__)


@dataclass
class OAuthState:
    settings: OAuthSettings

    def __post_init__(self) -> None:
        self.client = OAuth()
        self._register_providers()

    def _register_providers(self) -> None:
        for provider in self.settings.providers:
            self.client.register(**asdict(provider))
            logger.debug(f'Oauth provider [{provider.name}] has been registered.')
