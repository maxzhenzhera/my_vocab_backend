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

from ...api.dependencies.mail import MailSenderMarker
from ...resources.mail.subjects import (
    CONFIRMATION_MAIL_SUBJECT,
    CREDENTIALS_MAIL_SUBJECT
)
from ...schemas.entities.user import UserInResponse
from ...services.authentication.oauth.dataclasses_ import OAuthUserCredentials


__all__ = ['MailService']


warnings.warn(
    UserWarning(
        'Emails will be built for the LOCAL DEVELOPMENT. '
        'For production: programmer has to provide a new implementation!'
    )
)


logger = logging.getLogger(__name__)


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
            'email_confirmation_url': ''.join(
                (
                    self._make_email_confirmation_url(),
                    f'?token={user.email_confirmation_token}'
                )
            )
        }

    def _make_email_confirmation_url(self) -> str:
        return self.request.url_for(name='auth:confirm')

    def send_credentials_mail(self, credentials: OAuthUserCredentials) -> None:
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
    def _make_credentials_mail(credentials: OAuthUserCredentials) -> MessageSchema:
        return MessageSchema(
            subject=CREDENTIALS_MAIL_SUBJECT,
            recipients=[credentials.email],
            template_body={'credentials': credentials}
        )
