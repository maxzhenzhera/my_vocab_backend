from httpx import (
    AsyncClient,
    Response
)

from app.core.config import jwt_config
from app.main import app
from app.schemas.authentication import AuthenticationResult
from app.schemas.entities.user import UserInResponse
from tests.users import TestUser


__all__ = [
    'make_authenticated_client',
    'make_unauthenticated_client',
    'create_user',
    'get_user_from_client'
]


CLIENT_USER_ATTRIBUTE_NAME = 'custom_attribute__user'


async def make_authenticated_client(client: AsyncClient, user: TestUser) -> AsyncClient:
    unauthenticated_client = await make_unauthenticated_client(client, user)
    return await _authenticate_client(unauthenticated_client, user)


async def make_unauthenticated_client(client: AsyncClient, user: TestUser) -> AsyncClient:
    response = await create_user(client, user)
    user = UserInResponse(**response.json())
    _set_user_in_client(client, user)
    return client


async def create_user(client: AsyncClient, user: TestUser) -> Response:
    return await client.post(app.url_path_for('auth:create'), json=user.in_create.dict())


def _set_user_in_client(client: AsyncClient, authentication_result: UserInResponse) -> None:
    setattr(client, CLIENT_USER_ATTRIBUTE_NAME, authentication_result)


def get_user_from_client(client: AsyncClient) -> UserInResponse:
    return getattr(client, CLIENT_USER_ATTRIBUTE_NAME)


async def _authenticate_client(client: AsyncClient, user: TestUser) -> AsyncClient:
    response = await _send_login_request(client, user)
    authentication_result = AuthenticationResult(**response.json())
    _set_access_token_in_authorization_header(client, authentication_result.tokens.access_token.token)
    return client


async def _send_login_request(client: AsyncClient, user: TestUser) -> Response:
    return await client.post(app.url_path_for('auth:login'), json=user.in_login.dict())


def _set_access_token_in_authorization_header(client: AsyncClient, access_token: str) -> None:
    client.headers['Authorization'] = f'{jwt_config.ACCESS_TOKEN_TYPE} {access_token}'
