import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.db.events import _set_db_in_app                        # noqa ; not in __all__; access to a protected member
from app.services.mail.events import _set_mail_sender_in_app    # noqa ; not in __all__; access to a protected member
from tests.config import (
    sqlalchemy_connection_string_to_test_database,
    mail_connection_test_config
)
from tests.helpers.db import create_clear_db


@pytest.fixture(name='app')
def fixture_app() -> FastAPI:
    from app.main import app

    return app


@pytest.fixture(name='test_app')
async def fixture_test_app(app: FastAPI) -> FastAPI:
    _set_mail_sender_in_app(mail_connection_test_config, app)
    _set_db_in_app(sqlalchemy_connection_string_to_test_database, app)
    await create_clear_db(app)
    return app


@pytest.fixture(name='test_client')
async def fixture_client(test_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=test_app,
        base_url=f"http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client
