import pytest
from fastapi import FastAPI
from fastapi_mail import FastMail
from httpx import AsyncClient

from app.core.config import mail_connection_config
from app.db.models import Base
from app.db.postgres import (
    create_engine,
    create_sessionmaker
)
from tests.env import sqlalchemy_connection_string_to_test_database


@pytest.fixture(name='app')
def fixture_app() -> FastAPI:
    from app.main import app

    return app


@pytest.fixture(name='test_app')
async def fixture_test_app(app: FastAPI) -> FastAPI:
    # set mail sender config for suppress sending
    app.state.mail_sender = FastMail(mail_connection_config)
    app.state.mail_sender.config.SUPPRESS_SEND = 1
    # put connection to test database
    app.state.db_engine = create_engine(sqlalchemy_connection_string_to_test_database)
    app.state.db_sessionmaker = create_sessionmaker(app.state.db_engine)
    # drop and create tables in test database
    async with app.state.db_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    return app


@pytest.fixture(name='test_client')
async def fixture_client(test_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=test_app,
        base_url=f"http://testserver",   # noqa
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client
