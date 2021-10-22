from httpx import (
    AsyncClient,
    Response
)

from app.main import app
from app.schemas.authentication import AuthenticationResult
from app.schemas.jwt import AccessTokenInResponse
from app.schemas.user import UserInResponse
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
    login_response = await _send_login_request(unauthenticated_client, user)
    return _authenticate_client(unauthenticated_client, login_response)


async def make_unauthenticated_client(client: AsyncClient, user: TestUser) -> AsyncClient:
    create_response = await create_user(client, user)
    user = UserInResponse(**create_response.json())
    _set_user_in_client(client, user)
    return client


async def create_user(client: AsyncClient, user: TestUser) -> Response:
    return await client.post(app.url_path_for('auth:create'), json=user.in_create.dict())


def _set_user_in_client(client: AsyncClient, authentication_result: UserInResponse) -> None:
    setattr(client, CLIENT_USER_ATTRIBUTE_NAME, authentication_result)


def get_user_from_client(client: AsyncClient) -> UserInResponse:
    return getattr(client, CLIENT_USER_ATTRIBUTE_NAME)


async def _send_login_request(client: AsyncClient, user: TestUser) -> Response:
    return await client.post(app.url_path_for('auth:login'), json=user.in_login.dict())


def _authenticate_client(client: AsyncClient, login_response: Response) -> AsyncClient:
    authentication_result = AuthenticationResult(**login_response.json())
    _set_access_token_in_authorization_header(client, authentication_result.tokens.access_token)
    return client


def _set_access_token_in_authorization_header(client: AsyncClient, access_token: AccessTokenInResponse) -> None:
    client.headers['Authorization'] = f'{access_token.token_type} {access_token.token}'
