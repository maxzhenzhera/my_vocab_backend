from httpx import AsyncClient

from app.db.repositories import OAuthConnectionsRepository
from .auth import get_user_from_client
from ..users import TestUser


__all__ = ['link_oauth_connections']


async def link_oauth_connections(
        oauth_connections_repository: OAuthConnectionsRepository,
        client: AsyncClient,
        test_user: TestUser
) -> None:
    created_user = get_user_from_client(client)

    async with oauth_connections_repository.session.begin():
        for oauth_connection in test_user.get_oauth_connections(created_user.id):
            await oauth_connections_repository.link_connection(oauth_connection)
