from fastapi import FastAPI
from httpx import AsyncClient

from app.schemas.authentication import AuthenticationResult
from app.schemas.entities.user import UserInResponse
from ..dataclasses_ import MetaUser


__all__ = [
    'set_user_in_client',
    'get_user_from_client',
    'make_unauthenticated_client',
    'authenticate_client'
]


_USER_ATTRIBUTE_NAME = 'custom_attribute__user'


def set_user_in_client(
        user: UserInResponse,
        client: AsyncClient
) -> None:
    setattr(client, _USER_ATTRIBUTE_NAME, user)


def get_user_from_client(client: AsyncClient) -> UserInResponse:
    return getattr(client, _USER_ATTRIBUTE_NAME)  # type: ignore[no-any-return]


async def make_unauthenticated_client(
        app: FastAPI,
        client: AsyncClient,
        meta_user: MetaUser
) -> AsyncClient:
    user = await _send_create_user_request(app, client, meta_user)
    set_user_in_client(user, client)
    return client


async def _send_create_user_request(
        app: FastAPI,
        client: AsyncClient,
        meta_user: MetaUser
) -> UserInResponse:
    response = await client.post(
        url=app.url_path_for('auth:create'),
        json=meta_user.in_create.dict()
    )
    return UserInResponse(**response.json())


async def authenticate_client(
        app: FastAPI,
        client: AsyncClient,
        meta_user: MetaUser
) -> AsyncClient:
    authentication_result = await _send_login_request(app, client, meta_user)
    _set_access_token_in_authorization_header(
        client=client,
        access_token=authentication_result.access_token
    )
    return client


async def _send_login_request(
        app: FastAPI,
        client: AsyncClient,
        meta_user: MetaUser
) -> AuthenticationResult:
    response = await client.post(
        url=app.url_path_for('auth:login'),
        json=meta_user.in_login.dict()
    )
    return AuthenticationResult(**response.json())


def _set_access_token_in_authorization_header(
        client: AsyncClient,
        access_token: str
) -> None:
    client.headers['Authorization'] = f'Bearer {access_token}'
