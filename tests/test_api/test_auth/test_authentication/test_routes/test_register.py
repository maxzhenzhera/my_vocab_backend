from collections.abc import AsyncGenerator
from email.mime.multipart import MIMEMultipart
from typing import ClassVar

import pytest
from fastapi_mail import FastMail
from httpx import AsyncClient
from starlette.datastructures import URLPath

from app.main import app
from app.services.mail.subjects import CONFIRMATION_MAIL_SUBJECT
from ..base import BaseTestUserCreationRoute
from ...base import BaseTestAuthRoute
from ...base import BaseTestEmailSendingRoute
from ....mixins.response_and_client import ResponseAndClient
from .....users import test_user_1


pytestmark = pytest.mark.asyncio


class TestRegisterRoute(BaseTestAuthRoute, BaseTestUserCreationRoute, BaseTestEmailSendingRoute):
    url: ClassVar[URLPath] = app.url_path_for('auth:register')
    request_json: ClassVar[dict] = test_user_1.in_create.dict()
    number_emails_sent: ClassVar[int] = 1
    created_user_email: ClassVar[str] = test_user_1.email

    @pytest.fixture(name='response_and_client')
    async def fixture_response_and_client(self, test_client: AsyncClient) -> ResponseAndClient:
        return await test_client.post(self.url, json=self.request_json), test_client

    @pytest.fixture(name='email_outbox')
    async def fixture_email_outbox(
            self,
            test_mail_sender: FastMail,
            test_client: AsyncClient
    ) -> AsyncGenerator[list[MIMEMultipart], None]:
        with test_mail_sender.record_messages() as outbox:
            await test_client.post(self.url, json=self.request_json)
            yield outbox

    async def test_confirmation_email_sending(self, email_outbox: list[MIMEMultipart]):
        self._test_base_outbox_claims(email_outbox)

        confirmation_mail = email_outbox[0]
        assert confirmation_mail['To'] == self.created_user_email
        assert confirmation_mail['Subject'] == CONFIRMATION_MAIL_SUBJECT
