import logging

from fastapi import FastAPI
from fastapi_mail import FastMail

from ...core.config.config import mail_connection_config


__all__ = ['init_mail_sender']


logger = logging.getLogger(__name__)


def init_mail_sender(app: FastAPI) -> None:
    app.state.mail_sender = FastMail(mail_connection_config)
    logger.info('Mail sender has been set.')
