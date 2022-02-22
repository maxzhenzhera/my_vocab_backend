import logging

from fastapi import FastAPI
from fastapi_mail import ConnectionConfig as MailConnectionSettings

from .state import MailState


__all__ = ['init_mail']


logger = logging.getLogger(__name__)


def init_mail(app: FastAPI, settings: MailConnectionSettings) -> None:
    app.state.mail = MailState(settings)
    logger.info('Mail state (sender) has been set.')
