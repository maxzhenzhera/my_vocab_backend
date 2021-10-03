import logging

from fastapi import FastAPI
from fastapi_mail import (
    FastMail,
    ConnectionConfig as MailConnectionConfig
)

from ...core.config.config import mail_connection_config


__all__ = ['init_mail_sender']


logger = logging.getLogger(__name__)


def init_mail_sender(app: FastAPI) -> None:
    _set_mail_sender_in_app(mail_connection_config, app)
    logger.info('Mail sender has been set.')


def _set_mail_sender_in_app(config: MailConnectionConfig, app: FastAPI) -> None:
    app.state.mail_sender = FastMail(config)
