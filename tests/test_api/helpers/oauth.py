from httpx import AsyncClient

from app.db.models import User
from app.db.repos import OAuthConnectionsRepo
from .auth import get_user_from_client
from ..dataclasses_ import MetaUser


__all__ = ['link_oauth_connections']


async def link_oauth_connections(
        oauth_connections_repo: OAuthConnectionsRepo,
        client: AsyncClient,
        meta_user: MetaUser
) -> None:
    created_user = get_user_from_client(client)

    async with oauth_connections_repo.session.begin():
        await oauth_connections_repo.link_google_connection(
            oauth_user=meta_user.google_oauth_user,
            internal_user=User(id=created_user.id)
        )
