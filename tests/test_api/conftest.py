"""
Fixtures:
    +-- app settings
    +-- migrations
        +-- config
        +-- applying migrations
    +-- app
        +-- just built app
        +-- fully initialized app
    +-- meta users
        +-- user 1
    +-- clients
        +-- simple test client for app
        +-- unauthenticated
            +-- without OAuth
                +-- client for user 1
            +-- with OAuth
                +-- client for user 1
        +-- authenticated
            +-- without OAuth
                +-- client for user 1
            +-- with OAuth
                +-- client for user 1
    +-- created users
        +-- user 1
    +-- mail sender
    +-- db
        +-- components
            +-- sessionmaker
            +-- session
        +-- repos
            +-- OAuthConnectionsRepo
            +-- RefreshSessionsRepo
            +-- UsersRepo
"""

from __future__ import annotations  # https://github.com/sqlalchemy/sqlalchemy/issues/7656

from collections.abc import AsyncGenerator

import pytest
from alembic.command import (
    downgrade as alembic_downgrade,
    upgrade as alembic_upgrade,
)
from alembic.config import Config as AlembicConfig
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from fastapi_mail import FastMail
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.factory import get_app
from app.core.config import get_app_settings
from app.core.settings import AppSettings
from app.core.settings.environment import AppEnvType
from app.core.settings.paths import ALEMBIC_CONFIG_PATH
from app.db.repos import (
    OAuthConnectionsRepo,
    RefreshSessionsRepo,
    UsersRepo
)
from app.schemas.entities.user import UserInResponse
from .dataclasses_ import MetaUser
from .helpers.auth import (
    authenticate_client,
    get_user_from_client,
    make_unauthenticated_client
)
from .helpers.oauth import link_oauth_connections


# ////////////////////////////////////////////////////////////////////////////////////////
# Fixtures: app settings


@pytest.fixture(name='app_settings', scope='session')
def fixture_app_settings() -> AppSettings:
    return get_app_settings(AppEnvType.TEST)


# ////////////////////////////////////////////////////////////////////////////////////////
# Fixtures: migrations


@pytest.fixture(name='alembic_config', scope='session')
def fixture_alembic_config(app_settings: AppSettings) -> AlembicConfig:
    config = AlembicConfig(str(ALEMBIC_CONFIG_PATH))
    config.set_main_option('sqlalchemy.url', app_settings.db.sqlalchemy_url)
    return config


@pytest.fixture(name='apply_migrations')
def fixture_apply_migrations(alembic_config: AlembicConfig) -> None:
    alembic_upgrade(alembic_config, 'head')
    yield
    alembic_downgrade(alembic_config, 'base')


# ////////////////////////////////////////////////////////////////////////////////////////
# Fixtures: app


@pytest.fixture(name='app')
def fixture_app(app_settings: AppSettings, apply_migrations: None) -> FastAPI:
    return get_app(app_settings)


@pytest.fixture(name='initialized_app')
async def fixture_initialized_app(app: FastAPI) -> AsyncGenerator[FastAPI, None]:
    async with LifespanManager(app):
        yield app


# ////////////////////////////////////////////////////////////////////////////////////////
# Fixtures: meta users


@pytest.fixture(name='meta_user_1', scope='session')
def fixture_meta_user_1() -> MetaUser:
    return MetaUser(
        email='user1@gmail.com',
        password='user1Password',
        google_id='user1GoogleID'
    )


# ////////////////////////////////////////////////////////////////////////////////////////
# Fixtures: clients


@pytest.fixture(name='client')
async def fixture_client(initialized_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
            app=initialized_app,
            base_url='http://testserver',
            headers={"Content-Type": "application/json"},
    ) as client:
        yield client


# # Fixtures: unauthenticated ------------------------------------------------------------

# # # Fixtures: without OAuth ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


@pytest.fixture(name='unauthenticated_client_1')
async def fixture_unauthenticated_client_1(
        app: FastAPI,
        client: AsyncClient,
        oauth_connections_repo: OAuthConnectionsRepo,
        meta_user_1: MetaUser
) -> AsyncClient:
    unauthenticated_client_1 = await make_unauthenticated_client(
        app=app,
        client=client,
        meta_user=meta_user_1
    )
    await link_oauth_connections(
        oauth_connections_repo=oauth_connections_repo,
        client=unauthenticated_client_1,
        meta_user=meta_user_1
    )
    return unauthenticated_client_1


# # # Fixtures: with OAuth +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


@pytest.fixture(name='unauthenticated_client_1_with_oauth')
async def fixture_unauthenticated_client_1_with_oauth(
        unauthenticated_client_1: AsyncClient,
        oauth_connections_repo: OAuthConnectionsRepo,
        meta_user_1: MetaUser
) -> AsyncClient:
    await link_oauth_connections(
        oauth_connections_repo=oauth_connections_repo,
        client=unauthenticated_client_1,
        meta_user=meta_user_1
    )
    return unauthenticated_client_1


# # Fixtures: authenticated --------------------------------------------------------------

# # # Fixtures: without OAuth ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


@pytest.fixture(name='client_1')
async def fixture_client_1(
        app: FastAPI,
        unauthenticated_client_1: AsyncClient,
        meta_user_1: MetaUser
) -> AsyncClient:
    return await authenticate_client(
        app=app,
        client=unauthenticated_client_1,
        meta_user=meta_user_1
    )


# # # Fixtures: with OAuth +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


@pytest.fixture(name='client_1_with_oauth')
async def fixture_client_1_with_oauth(
        app: FastAPI,
        unauthenticated_client_1_with_oauth: AsyncClient,
        meta_user_1: MetaUser
) -> AsyncClient:
    return await authenticate_client(
        app=app,
        client=unauthenticated_client_1_with_oauth,
        meta_user=meta_user_1
    )


# ////////////////////////////////////////////////////////////////////////////////////////
# Fixtures: created users


@pytest.fixture(name='user_1')
def fixture_user_1(client_1: AsyncClient) -> UserInResponse:
    return get_user_from_client(client_1)


# ////////////////////////////////////////////////////////////////////////////////////////
# Fixtures: mail sender


@pytest.fixture(name='mail_sender')
def fixture_mail_sender(initialized_app: FastAPI) -> FastMail:
    return initialized_app.state.mail.sender


# ////////////////////////////////////////////////////////////////////////////////////////
# Fixtures: db

# # Fixtures: components -----------------------------------------------------------------


@pytest.fixture(name='db_sessionmaker')
def fixture_sessionmaker(initialized_app: FastAPI) -> sessionmaker[AsyncSession]:
    return initialized_app.state.db.sessionmaker  # type: ignore[no-any-return]


@pytest.fixture(name='db_session')
async def fixture_db_session(
        db_sessionmaker: sessionmaker[AsyncSession]
) -> AsyncGenerator[AsyncSession, None]:
    async with db_sessionmaker() as session:
        yield session


# # Fixtures: repos ----------------------------------------------------------------------


@pytest.fixture(name='oauth_connections_repo')
def fixture_oauth_connections_repo(db_session: AsyncSession) -> OAuthConnectionsRepo:
    return OAuthConnectionsRepo(db_session)


@pytest.fixture(name='refresh_sessions_repo')
def fixture_refresh_sessions_repo(db_session: AsyncSession) -> RefreshSessionsRepo:
    return RefreshSessionsRepo(db_session)


@pytest.fixture(name='users_repo')
def fixture_users_repo(db_session: AsyncSession) -> UsersRepo:
    return UsersRepo(db_session)
