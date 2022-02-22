import logging
import warnings
from dataclasses import dataclass

from fastapi import (
    BackgroundTasks,
    Depends,
    Request
)
from fastapi_mail import (
    FastMail,
    MessageSchema
)


from ...resources.mail.subjects import (
    CONFIRMATION_MAIL_SUBJECT,
    CREDENTIALS_MAIL_SUBJECT
)
from ...api.dependencies.mail import MailSenderMarker
from ...schemas.entities.user import (
    UserInLogin,
    UserInResponse
)


__all__ = ['MailService']


logger = logging.getLogger(__name__)

warnings.warn(
    'Emails will be built for the LOCAL DEVELOPMENT. '
    'For production: programmer has to provide a new implementation!'
)


@dataclass
class MailService:
    request: Request
    background_tasks: BackgroundTasks
    mail_sender: FastMail = Depends(MailSenderMarker)

    def send_confirmation_mail(self, user: UserInResponse) -> None:
        self.background_tasks.add_task(
            self.mail_sender.send_message,
            message=self._make_confirmation_mail(user),
            template_name='confirmation.html'
        )
        logger.info(
            f'Confirmation mail sending for {user.email} '
            'has been pushed in background tasks.'
        )

    def _make_confirmation_mail(self, user: UserInResponse) -> MessageSchema:
        return MessageSchema(
            subject=CONFIRMATION_MAIL_SUBJECT,
            recipients=[user.email],
            template_body=self._make_body_for_confirmation_mail(user)
        )

    def _make_body_for_confirmation_mail(
            self,
            user: UserInResponse
    ) -> dict[str, str | UserInResponse]:
        return {
            'user': user,
            'email_confirmation_url': self._make_email_confirmation_url(
                user.email_confirmation_token
            )
        }

    def _make_email_confirmation_url(self, token: str) -> str:
        return self.request.app.url_path_for(
            name='auth:confirm',
            token=token
        )

    def send_credentials_mail(self, credentials: UserInLogin) -> None:
        self.background_tasks.add_task(
            self.mail_sender.send_message,
            self._make_credentials_mail(credentials),
            template_name='credentials.html'
        )
        logger.info(
            f'Credentials mail sending for {credentials.email} '
            'has been pushed in background tasks.'
        )

    @staticmethod
    def _make_credentials_mail(credentials: UserInLogin) -> MessageSchema:
        return MessageSchema(
            subject=CREDENTIALS_MAIL_SUBJECT,
            recipients=[credentials.email],
            template_body={'credentials': credentials}
        )
