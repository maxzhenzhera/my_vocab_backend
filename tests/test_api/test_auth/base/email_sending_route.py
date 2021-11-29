from abc import (
    ABC,
    abstractmethod
)
from collections.abc import AsyncGenerator
from email.mime.multipart import MIMEMultipart

import pytest
from fastapi_mail import FastMail

from ...base import BaseTestRoute
from ....config import mail_connection_test_config


__all__ = ['BaseTestEmailSendingRoute']


class BaseTestEmailSendingRoute(BaseTestRoute, ABC):
    @property
    @abstractmethod
    def number_emails_sent(self) -> int:
        """
        The number of sent emails per API request.

        Abstract *class* attribute:
            number_emails_sent: ClassVar[int] = 1       # or whatever number that suits
        """

    @pytest.fixture(name='email_outbox')
    @abstractmethod
    def fixture_email_outbox(
            self,
            test_mail_sender: FastMail,
            *args
    ) -> AsyncGenerator[list[MIMEMultipart], None]:
        """
        Abstract fixture that must return the email outbox
        that has handled API request (means context manager).

            .. code-block:: python

                    with test_mail_sender.record_messages() as outbox:
                        # here execute request to API; e.g.:
                        await test_client.post(self.url, json=self.request_json)

                        yield outbox
        """

    def _test_base_outbox_claims(self, email_outbox: list[MIMEMultipart]):
        self._test_outbox_length(email_outbox)
        self._test_outbox_sender(email_outbox)

    def _test_outbox_length(self, email_outbox: list[MIMEMultipart]):
        assert len(email_outbox) == self.number_emails_sent

    @staticmethod
    def _test_outbox_sender(email_outbox: list[MIMEMultipart]):
        for mail in email_outbox:
            if mail_connection_test_config.MAIL_FROM_NAME is not None:
                from_ = (
                    f"{mail_connection_test_config.MAIL_FROM_NAME} "
                    f"<{mail_connection_test_config.MAIL_FROM}>"
                )
                assert mail['from'] == from_
            else:
                from_ = mail_connection_test_config.MAIL_FROM
                assert mail['from'] == from_
