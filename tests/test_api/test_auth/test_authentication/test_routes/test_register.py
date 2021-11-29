from typing import ClassVar

import pytest
from httpx import AsyncClient
from starlette.datastructures import URLPath

from app.main import app
from ..base import (
    BaseTestAuthRoute,
    BaseTestUserCreationRoute
)
from ...base import BaseTestPostRoute
from ...mixins.response_and_client import ResponseAndClient
from ....config import mail_connection_test_config
from ....users import test_user_1


pytestmark = pytest.mark.asyncio


class TestRegisterRoute(BaseTestAuthRoute, BaseTestUserCreationRoute, BaseTestPostRoute):
    url: ClassVar[URLPath] = app.url_path_for('auth:register')
    request_json: ClassVar[dict] = test_user_1.in_create.dict()
    created_user_email: ClassVar[str] = test_user_1.email

    @pytest.fixture(name='response_and_client')
    async def fixture_response_and_client(self, test_client: AsyncClient) -> ResponseAndClient:
        return await test_client.post(self.url, json=self.request_json), test_client

    async def test_email_sending(self, test_mail_sender, test_client: AsyncClient):
        with test_mail_sender.record_messages() as outbox:
            _ = await test_client.post(self.url, json=self.request_json)

            assert len(outbox) == 1
            if mail_connection_test_config.MAIL_FROM_NAME is not None:
                from_ = (
                    f"{mail_connection_test_config.MAIL_FROM_NAME} "
                    f"<{mail_connection_test_config.MAIL_FROM}>"
                )
                assert outbox[0]['from'] == from_
            else:
                from_ = mail_connection_test_config.MAIL_FROM
                assert outbox[0]['from'] == from_
            assert outbox[0]['To'] == self.created_user_email
