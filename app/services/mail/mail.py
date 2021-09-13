from dataclasses import dataclass

from fastapi import (
    BackgroundTasks,
    Depends
)
from fastapi_mail import (
    FastMail,
    MessageSchema
)

from ...api.dependencies.mail import get_mail_sender
from ...schemas.user import UserInResponse


@dataclass
class MailService:
    background_tasks: BackgroundTasks
    mail_sender: FastMail = Depends(get_mail_sender)

    def send_activation_mail(self, user: UserInResponse) -> None:
        self.background_tasks.add_task(self.mail_sender.send_message, self._make_activation_mail(user))

    @staticmethod
    def _make_activation_mail(user: UserInResponse) -> MessageSchema:
        return MessageSchema(
            subject='Account email confirmation',
            recipients=[user.email],
            body=f'Here is a activation link: {user.activation_link}'
        )
