import logging
import warnings
from dataclasses import dataclass
from uuid import UUID

from fastapi import (
    BackgroundTasks,
    Depends
)
from fastapi_mail import (
    FastMail,
    MessageSchema
)

from ...api.dependencies.mail import get_mail_sender
from ...core.config.config import server_config
from ...schemas.user import UserInResponse


__all__ = ['MailService']


logger = logging.getLogger(__name__)


@dataclass
class MailService:
    background_tasks: BackgroundTasks
    mail_sender: FastMail = Depends(get_mail_sender)

    def send_confirmation_mail(self, user: UserInResponse) -> None:
        self.background_tasks.add_task(
            self.mail_sender.send_message,
            self._make_confirmation_mail(user),
            template_name='confirmation.html'
        )
        logger.info(f'Confirmation mail sending for {user.email} has been pushed in background tasks.')

    def _make_confirmation_mail(self, user: UserInResponse) -> MessageSchema:
        return MessageSchema(
            subject='Account email confirmation',
            recipients=[user.email],
            template_body=self._make_template_body_for_confirmation_mail(user)
        )

    def _make_template_body_for_confirmation_mail(self, user: UserInResponse) -> dict:
        return {
                'user': user,
                'email_confirmation_link': self._make_email_confirmation_link(user.email_confirmation_link)
            }

    @staticmethod
    def _make_email_confirmation_link(link: UUID) -> str:
        warnings.warn(
            'Email confirmation link has created for the LOCAL DEVELOPMENT. '
            'For production programmer has to make a new implementation!'
        )
        return (
            f'http://localhost:{server_config.PORT}'
            f'{server_config.API_PREFIX}/auth/confirm?link={link}'
        )
