from abc import (
    ABC,
    abstractmethod
)
from collections.abc import AsyncGenerator
from email.mime.multipart import MIMEMultipart
from typing import ClassVar
from unittest.mock import MagicMock

import pytest
from fastapi_mail import FastMail
from httpx import AsyncClient
from starlette.status import HTTP_400_BAD_REQUEST

from app.db.repositories import OAuthConnectionsRepository
from app.services.mail.subjects import CREDENTIALS_MAIL_SUBJECT
from .oauth_route import BaseTestOAuthRoute
from .oauth_user_creation_route import BaseTestOAuthUserCreationRoute
from ...base import BaseTestEmailSendingRoute
from ....mixins.response_and_client import ResponseAndClient


__all__ = ['BaseOauthRegisterRoute']


class BaseOauthRegisterRoute(
    BaseTestOAuthRoute,
    BaseTestOAuthUserCreationRoute,
    BaseTestEmailSendingRoute,
    ABC
):
    number_emails_sent: ClassVar[int] = 1

    @pytest.fixture(name='response_and_client')
    async def fixture_response_and_client(
            self,
            mock_get_oauth_user: MagicMock,
            test_client: AsyncClient
    ) -> ResponseAndClient:
        return await test_client.get(self.url), test_client

    @pytest.mark.usefixtures('mock_get_oauth_user')
    @abstractmethod
    async def test_creating_oauth_connection_in_db(
            self,
            test_oauth_connections_repository: OAuthConnectionsRepository,
            client: AsyncClient,
    ):
        """
        On route execution oauth connection must be linked to user.
        So, it must be oauth connection record in db.
        """

    @pytest.mark.usefixtures('mock_get_oauth_user')
    async def test_return_400_error_on_passing_already_used_credentials(
            self,
            client: AsyncClient
    ):
        response = await client.get(self.url)

        assert response.status_code == HTTP_400_BAD_REQUEST

    @pytest.fixture(name='email_outbox')
    async def fixture_email_outbox(
            self,
            mock_get_oauth_user: MagicMock,
            test_mail_sender: FastMail,
            test_client: AsyncClient
    ) -> AsyncGenerator[list[MIMEMultipart], None]:
        with test_mail_sender.record_messages() as outbox:
            await test_client.get(self.url)
            yield outbox

    async def test_credentials_email_sending(self, email_outbox: list[MIMEMultipart]):
        self._test_base_outbox_claims(email_outbox)

        credentials_mail = email_outbox[0]
        assert credentials_mail['To'] == self.created_user_email
        assert credentials_mail['Subject'] == CREDENTIALS_MAIL_SUBJECT
