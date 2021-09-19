from fastapi import Request
from fastapi_mail import FastMail


__all__ = ['get_mail_sender']


def get_mail_sender(request: Request) -> FastMail:
    return request.app.state.mail_sender
