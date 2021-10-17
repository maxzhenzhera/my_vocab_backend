from httpx import (
    AsyncClient,
    Response
)

from app.main import app
from tests.users import TestUser


__all__ = [
    'make_unauthenticated_client',
    'make_authenticated_client',
    'create_user'
]


async def make_unauthenticated_client(client: AsyncClient, user: TestUser) -> AsyncClient:
    await create_user(client, user)
    return client


async def create_user(client: AsyncClient, user: TestUser) -> Response:
    return await client.post(app.url_path_for('auth:create'), json=user.in_create.dict())


async def make_authenticated_client(client: AsyncClient, user: TestUser) -> AsyncClient:
    response = await register_user(client, user)
    _set_access_token_in_authorization_header(client, response.json())
    return client


async def register_user(client: AsyncClient, user: TestUser) -> Response:
    return await client.post(app.url_path_for('auth:register'), json=user.in_create.dict())


def _set_access_token_in_authorization_header(client: AsyncClient, register_route_response_json: dict) -> None:
    client.headers['Authorization'] = f'Bearer {register_route_response_json["tokens"]["access_token"]["token"]}'
