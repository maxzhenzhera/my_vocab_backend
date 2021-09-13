from fastapi_mail import FastMail

from ...core.config import mail_connection_config


__all__ = ['get_mail_sender']


def get_mail_sender() -> FastMail:
    return FastMail(mail_connection_config)
