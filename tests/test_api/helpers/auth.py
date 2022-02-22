from httpx import AsyncClient

from app.core.settings.dataclasses_.components import JWTSettings
from app.schemas.authentication import AuthenticationResult
from app.schemas.entities.user import UserInResponse
from ..users import TestUser


__all__ = [
    'set_user_in_client',
    'get_user_from_client',
    'make_unauthenticated_client',
    'authenticate_client'
]


CLIENT_USER_ATTRIBUTE_NAME = 'custom_attribute__user'


def set_user_in_client(
        client: AsyncClient,
        user: UserInResponse
) -> None:
    setattr(client, CLIENT_USER_ATTRIBUTE_NAME, user)


def get_user_from_client(client: AsyncClient) -> UserInResponse:
    return getattr(client, CLIENT_USER_ATTRIBUTE_NAME)


async def make_unauthenticated_client(
        client: AsyncClient,
        user: TestUser
) -> AsyncClient:
    user = await _send_create_user_request(client, user)
    set_user_in_client(client, user)
    return client


async def _send_create_user_request(
        client: AsyncClient,
        user: TestUser
) -> UserInResponse:
    response = await client.post(
        # app.url_path_for('auth:create'),
        client._protocol.app.url_path_for('auth:create'),
        json=user.in_create.dict()
    )
    return UserInResponse(**response.json())


async def authenticate_client(
        client: AsyncClient,
        user: TestUser
) -> AsyncClient:
    authentication_result = await _send_login_request(client, user)
    _set_access_token_in_authorization_header(client, authentication_result.access_token)
    return client


async def _send_login_request(
        client: AsyncClient,
        user: TestUser
) -> AuthenticationResult:
    response = await client.post(
        # app.url_path_for('auth:login'),
        client._protocol.app.url_path_for('auth:login'),
        json=user.in_login.dict()
    )
    return AuthenticationResult(**response.json())


def _set_access_token_in_authorization_header(
        client: AsyncClient,
        access_token: str
) -> None:
    client.headers['Authorization'] = f'{JWTSettings.access_token.type} {access_token}'
