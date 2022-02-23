from collections.abc import AsyncGenerator
from email.mime.multipart import MIMEMultipart
from typing import (
    Any,
    ClassVar
)

import pytest
from fastapi_mail import FastMail
from httpx import AsyncClient
from starlette.datastructures import URLPath

from app.core.settings import AppSettings
from app.resources.mail.subjects import CONFIRMATION_MAIL_SUBJECT
from .base import BaseTestUserServerCreationRouteCase
from ..base import BaseTestAuthRouteCase
from ...dataclasses_ import MetaUser
from ...mixins.response_and_client import ResponseAndClient


pytestmark = pytest.mark.asyncio


class RegisterRouteNameMixin:
    route_name: ClassVar[str] = 'auth:register'


class TestRegisterRouteSingleCase(
    RegisterRouteNameMixin,
    BaseTestAuthRouteCase,
    BaseTestUserServerCreationRouteCase
):
    @pytest.fixture(name='created_user_email')
    def fixture_created_user_email(
            self,
            meta_user_1: MetaUser
    ) -> str:
        return meta_user_1.email

    @pytest.fixture(name='success_route_body')
    def fixture_success_route_body(
            self,
            meta_user_1: MetaUser
    ) -> dict[str, Any]:
        return meta_user_1.in_create.dict()

    @pytest.fixture(name='response_and_client_on_success')
    async def fixture_response_and_client_on_success(
            self,
            route_url: URLPath,
            success_route_body: dict[str, Any],
            client: AsyncClient
    ) -> ResponseAndClient:
        return (
            await client.post(
                url=route_url,
                json=success_route_body
            ),
            client
        )

    @pytest.fixture(name='email_outbox_on_success')
    async def fixture_email_outbox(
            self,
            route_url: URLPath,
            success_route_body: dict[str, Any],
            mail_sender: FastMail,
            client: AsyncClient
    ) -> AsyncGenerator[list[MIMEMultipart], None]:
        with mail_sender.record_messages() as outbox:
            await client.post(
                url=route_url,
                json=success_route_body
            )

            yield outbox

    async def test_confirmation_email_sending(
            self,
            created_user_email: str,
            email_outbox_on_success: list[MIMEMultipart],
            app_settings: AppSettings
    ):
        assert len(email_outbox_on_success) == 1

        confirmation_mail = email_outbox_on_success[0]
        assert confirmation_mail['To'] == created_user_email
        assert confirmation_mail['Subject'] == CONFIRMATION_MAIL_SUBJECT

        if app_settings.mail.MAIL_FROM_NAME is not None:
            from_ = (
                f"{app_settings.mail.MAIL_FROM_NAME} "
                f"<{app_settings.mail.MAIL_FROM}>"
            )
        else:
            from_ = app_settings.mail.MAIL_FROM
        assert confirmation_mail['from'] == from_
