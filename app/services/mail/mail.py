import logging
import warnings
from dataclasses import dataclass

from fastapi import (
    BackgroundTasks,
    Depends
)
from fastapi_mail import (
    FastMail,
    MessageSchema
)

from .subjects import (
    CONFIRMATION_MAIL_SUBJECT,
    CREDENTIALS_MAIL_SUBJECT
)
from ...api.dependencies.mail import get_mail_sender
from ...core.config import server_config
from ...schemas.entities.user import (
    UserInLogin,
    UserInResponse
)


__all__ = ['MailService']


logger = logging.getLogger(__name__)


@dataclass
class MailService:
    background_tasks: BackgroundTasks
    mail_sender: FastMail = Depends(get_mail_sender)

    @staticmethod
    def __post_init__() -> None:
        warnings.warn(
            'Emails will be built for the LOCAL DEVELOPMENT. '
            'For production programmer has to make a new implementation!'
        )

    def send_confirmation_mail(self, user: UserInResponse) -> None:
        self.background_tasks.add_task(
            self.mail_sender.send_message,
            self._make_confirmation_mail(user),
            template_name='confirmation.html'
        )
        logger.info(
            f'Confirmation mail sending for {user.email} has been pushed in background tasks.'
        )

    def _make_confirmation_mail(self, user: UserInResponse) -> MessageSchema:
        return MessageSchema(
            subject=CONFIRMATION_MAIL_SUBJECT,
            recipients=[user.email],
            template_body=self._make_template_body_for_confirmation_mail(user)
        )

    def _make_template_body_for_confirmation_mail(self, user: UserInResponse) -> dict:
        return {
                'user': user,
                'email_confirmation_link': self._make_email_confirmation_link(
                    user.email_confirmation_link
                )
            }

    @staticmethod
    def _make_email_confirmation_link(link: str) -> str:
        return (
            f'http://localhost:{server_config.PORT}'
            f'{server_config.API_PREFIX}/auth/confirm?link={link}'
        )

    def send_credentials_mail(self, credentials: UserInLogin) -> None:
        self.background_tasks.add_task(
            self.mail_sender.send_message,
            self._make_credentials_mail(credentials),
            template_name='credentials.html'
        )
        logger.info(
            f'Credentials mail sending for {credentials.email} has been pushed in background tasks.'
        )

    @staticmethod
    def _make_credentials_mail(credentials: UserInLogin) -> MessageSchema:
        return MessageSchema(
            subject=CREDENTIALS_MAIL_SUBJECT,
            recipients=[credentials.email],
            template_body={'credentials': credentials}
        )
