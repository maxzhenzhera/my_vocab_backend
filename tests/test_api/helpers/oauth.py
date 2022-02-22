from httpx import AsyncClient

from app.db.repos import OAuthConnectionsRepo
from .auth import get_user_from_client
from ..users import TestUser


__all__ = ['link_oauth_connections']


async def link_oauth_connections(
        oauth_connections_repo: OAuthConnectionsRepo,
        client: AsyncClient,
        user: TestUser
) -> None:
    created_user = get_user_from_client(client)

    async with oauth_connections_repo.session.begin():
        for oauth_connection in user.get_oauth_connections(created_user.id):
            await oauth_connections_repo.link_connection(oauth_connection)
