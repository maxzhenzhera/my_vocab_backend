from abc import ABC
from collections.abc import AsyncGenerator
from email.mime.multipart import MIMEMultipart
from unittest.mock import MagicMock

import pytest
from fastapi_mail import FastMail
from httpx import AsyncClient
from starlette.datastructures import URLPath
from starlette.status import HTTP_400_BAD_REQUEST

from app.core.settings import AppSettings
from app.resources.mail.subjects import CREDENTIALS_MAIL_SUBJECT
from .route import BaseTestOAuthRouteCaseWhenConnectionCreating
from .user_creation import BaseTestOAuthUserCreationRouteCase
from ....mixins.response_and_client import ResponseAndClient


__all__ = ['BaseOauthRegisterRouteCase']


class BaseOauthRegisterRouteCase(
    BaseTestOAuthRouteCaseWhenConnectionCreating,
    BaseTestOAuthUserCreationRouteCase,
    ABC
):
    @pytest.fixture(name='response_and_client_on_success')
    async def fixture_response_and_client_on_success(
            self,
            # apply mocking
            # -----------------------------
            mock_get_oauth_user: MagicMock,
            # -----------------------------
            route_url: URLPath,
            client: AsyncClient
    ) -> ResponseAndClient:
        return (
            await client.get(
                url=route_url
            ),
            client
        )

    @pytest.mark.usefixtures('mock_get_oauth_user')
    async def test_return_400_error_on_passing_already_used_credentials(
            self,
            route_url: URLPath,
            success_client: AsyncClient
    ):
        bad_response = await success_client.get(route_url)

        assert bad_response.status_code == HTTP_400_BAD_REQUEST

    @pytest.fixture(name='email_outbox_on_success')
    async def fixture_email_outbox(
            self,
            # apply mocking
            # -----------------------------
            mock_get_oauth_user: MagicMock,
            # -----------------------------
            route_url: URLPath,
            mail_sender: FastMail,
            client: AsyncClient
    ) -> AsyncGenerator[list[MIMEMultipart], None]:
        with mail_sender.record_messages() as outbox:
            await client.get(route_url)

            yield outbox

    async def test_credentials_email_sending(
            self,
            created_user_email: str,
            email_outbox_on_success: list[MIMEMultipart],
            app_settings: AppSettings
    ):
        assert len(email_outbox_on_success) == 1

        credentials_mail = email_outbox_on_success[0]
        assert credentials_mail['To'] == created_user_email
        assert credentials_mail['Subject'] == CREDENTIALS_MAIL_SUBJECT

        if app_settings.mail.MAIL_FROM_NAME is not None:
            from_ = (
                f"{app_settings.mail.MAIL_FROM_NAME} "
                f"<{app_settings.mail.MAIL_FROM}>"
            )
        else:
            from_ = app_settings.mail.MAIL_FROM
        assert credentials_mail['from'] == from_
