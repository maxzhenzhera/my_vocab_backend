from typing import TypeVar

from sqlalchemy import (
    delete as sa_delete,
    insert as sa_insert,
    update as sa_update
)
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.future import select as sa_select
from sqlalchemy.orm import joinedload

from .base import BaseRepository
from ..models import OAuthConnection
from ...schemas.authentication.oauth import BaseOAuthConnection


__all__ = ['OAuthConnectionsRepository']


class OAuthConnectionsRepository(BaseRepository):
    model = OAuthConnection

    async def link_connection(self, oauth_connection: BaseOAuthConnection) -> OAuthConnection:
        oauth_connection_on_insert = oauth_connection.dict()
        oauth_connection_on_conflict = {key: value for key, value in oauth_connection_on_insert.items() if key != 'user_id'}
        insert_stmt = pg_insert(OAuthConnection).values(**oauth_connection_on_insert)
        update_on_conflict_stmt = insert_stmt.on_conflict_do_update(
            index_elements=[OAuthConnection.user_id],
            set_=oauth_connection_on_conflict
        )
        return await self._return_from_statement(update_on_conflict_stmt)

    async def fetch_by_google_id_with_user(self, google_id: str) -> OAuthConnection:
        stmt = sa_select(OAuthConnection).options(joinedload(OAuthConnection.user)).\
            where(OAuthConnection.google_id == google_id)
        return await self._fetch_entity(stmt)
