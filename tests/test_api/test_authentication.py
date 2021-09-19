import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.core.config import mail_connection_config
from app.schemas.user import UserInCreate


pytestmark = pytest.mark.asyncio


async def test_register_route_result(app: FastAPI, test_client: AsyncClient):
    response = await test_client.post(
        app.url_path_for('auth:register'),
        json=UserInCreate(email='example@gmail.com', password='password').dict()  # noqa
    )
    response_json = response.json()

    assert response.status_code == 200
    assert 'user' in response_json and 'tokens' in response_json


async def test_register_route_refresh_token_cookie(app: FastAPI, test_client: AsyncClient):
    response = await test_client.post(
        app.url_path_for('auth:register'),
        json=UserInCreate(email='example@gmail.com', password='password').dict()  # noqa
    )

    assert response.status_code == 200
    assert 'refresh_token' in response.cookies


async def test_register_route_email_sending(app: FastAPI, test_client: AsyncClient):
    with test_client._transport.app.state.mail_sender.record_messages() as outbox:
        response = await test_client.post(
            app.url_path_for('auth:register'),
            json=UserInCreate(email='example@gmail.com', password='password').dict()  # noqa
        )

        assert response.status_code == 200

        assert len(outbox) == 1
        if mail_connection_config.MAIL_FROM_NAME is not None:
            assert outbox[0]['from'] == f"{mail_connection_config.MAIL_FROM_NAME} <{mail_connection_config.MAIL_FROM}>"
        else:
            assert outbox[0]['from'] == mail_connection_config.MAIL_FROM
        assert outbox[0]['To'] == "example@gmail.com"


async def test_register_route_raise_400(app: FastAPI, test_client: AsyncClient):
    _ = await test_client.post(
        app.url_path_for('auth:register'),
        json=UserInCreate(email='example@gmail.com', password='password').dict()  # noqa
    )
    response = await test_client.post(
        app.url_path_for('auth:register'),
        json=UserInCreate(email='example@gmail.com', password='password').dict()  # noqa
    )
    assert response.status_code == 400
