from dataclasses import dataclass

from fastapi_mail import (
    ConnectionConfig as MailConnectionSettings,
    FastMail
)


__all__ = ['MailState']


@dataclass
class MailState:
    settings: MailConnectionSettings

    def __post_init__(self) -> None:
        self.sender = FastMail(self.settings)
