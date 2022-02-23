import logging

from fastapi import FastAPI

from .state import OAuthState
from ....core.settings.dataclasses_.components import OAuthSettings


__all__ = ['init_oauth']


logger = logging.getLogger(__name__)


def init_oauth(app: FastAPI, settings: OAuthSettings) -> None:
    app.state.oauth = OAuthState(settings)
    logger.info('OAuth state (client) has been set.')
