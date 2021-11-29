from collections.abc import AsyncGenerator

import pytest
from fastapi import FastAPI
from fastapi_mail import FastMail
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.db.events import _set_db_in_app                        # noqa ; not in __all__; access to a protected member
from app.db.repositories import (
    OAuthConnectionsRepository,
    RefreshSessionsRepository,
    UsersRepository
)
from app.services.mail.events import _set_mail_sender_in_app    # noqa ; not in __all__; access to a protected member
from tests.config import (
    sqlalchemy_connection_string_to_test_database,
    mail_connection_test_config
)
from tests.helpers.auth import (
    make_unauthenticated_client,
    make_authenticated_client
)
from tests.helpers.db import (
    create_db,
    clear_db
)
from tests.helpers.oauth import link_oauth_connections
from tests.users import (
    test_user_1,
    test_user_2
)


# Fixtures: app, client


@pytest.fixture(name='app')
def fixture_app() -> FastAPI:
    from app.main import app

    return app


@pytest.fixture(name='test_app')
async def fixture_test_app(app: FastAPI) -> AsyncGenerator[FastAPI, None]:
    _set_mail_sender_in_app(mail_connection_test_config, app)
    _set_db_in_app(sqlalchemy_connection_string_to_test_database, app)
    await create_db(app)
    yield app
    await clear_db(app)


@pytest.fixture(name='test_client')
async def fixture_test_client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        app=test_app,
        base_url='http://testserver',
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


# Fixtures: unauthenticated client


@pytest.fixture(name='test_unauthenticated_client_user_1')
async def fixture_test_unauthenticated_client_user_1(test_client: AsyncClient) -> AsyncClient:
    return await make_unauthenticated_client(test_client, test_user_1)


@pytest.fixture(name='test_unauthenticated_client_user_1_with_oauth')
async def fixture_test_unauthenticated_client_user_1_with_oauth(
        test_client: AsyncClient,
        test_oauth_connections_repository: OAuthConnectionsRepository
) -> AsyncClient:
    client = await make_unauthenticated_client(test_client, test_user_1)
    await link_oauth_connections(
        test_oauth_connections_repository,
        client,
        test_user_1
    )
    return client


# Fixtures: authenticated clients


@pytest.fixture(name='test_client_user_1')
async def fixture_test_client_user_1(test_client: AsyncClient) -> AsyncClient:
    return await make_authenticated_client(test_client, test_user_1)


@pytest.fixture(name='test_client_user_2')
async def fixture_test_client_user_2(test_client: AsyncClient) -> AsyncClient:
    return await make_authenticated_client(test_client, test_user_2)


# Fixtures: dependencies - mail sender, db session


@pytest.fixture(name='test_mail_sender')
def fixture_test_mail_sender(test_app: FastAPI) -> FastMail:
    return test_app.state.mail_sender


@pytest.fixture(name='test_db_sessionmaker')
def fixture_test_db_sessionmaker(test_app: FastAPI) -> sessionmaker:
    return test_app.state.db_sessionmaker


@pytest.fixture(name='test_db_session')
async def fixture_test_db_session(
        test_db_sessionmaker: sessionmaker
) -> AsyncGenerator[AsyncSession, None]:
    async with test_db_sessionmaker() as session:
        yield session


# Fixtures: db repositories


@pytest.fixture(name='test_users_repository')
def fixture_test_users_repository(
        test_db_session: AsyncSession
) -> UsersRepository:
    return UsersRepository(test_db_session)


@pytest.fixture(name='test_refresh_sessions_repository')
def fixture_test_refresh_sessions_repository(
        test_db_session: AsyncSession
) -> RefreshSessionsRepository:
    return RefreshSessionsRepository(test_db_session)


@pytest.fixture(name='test_oauth_connections_repository')
def fixture_test_oauth_connections_repository(
        test_db_session: AsyncSession
) -> OAuthConnectionsRepository:
    return OAuthConnectionsRepository(test_db_session)
