from fastapi_mail import FastMail

from .markers import MailSenderMarker
from ....builder import AppBuilder


__all__ = ['inject_mail']


def inject_mail(builder: AppBuilder) -> None:
    def depend_on_mail() -> FastMail:
        return builder.app.state.mail.sender

    builder.app.dependency_overrides[MailSenderMarker] = depend_on_mail
