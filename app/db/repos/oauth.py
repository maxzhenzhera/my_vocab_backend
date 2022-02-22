from typing import ClassVar

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.future import select as sa_select
from sqlalchemy.orm import joinedload

from .base import BaseRepo
from ..models import (
    OAuthConnection,
    User
)
from ...services.authentication.oauth.dataclasses_ import OAuthUser


__all__ = ['OAuthConnectionsRepo']


class OAuthConnectionsRepo(BaseRepo[OAuthConnection]):
    model: ClassVar = OAuthConnection

    async def link_google_connection(
            self,
            oauth_user: OAuthUser,
            internal_user: User
    ) -> OAuthConnection:
        oauth_connection_on_insert: dict[str, str | int] = {
            # OAuthConnection.user_id
            'user_id': internal_user.id,
            # OAuthConnection.google_id
            'google_id': oauth_user.id
        }
        return await self._link_connection(oauth_connection_on_insert)

    async def _link_connection(
            self,
            oauth_connection_on_insert: dict[str, str | int]
    ) -> OAuthConnection:
        oauth_connection_on_conflict = oauth_connection_on_insert.copy()
        oauth_connection_on_conflict.pop('user_id')

        insert_stmt = (
            pg_insert(OAuthConnection)
            .values(**oauth_connection_on_insert)
        )
        update_on_conflict_stmt = (
            insert_stmt
            .on_conflict_do_update(
                index_elements=[OAuthConnection.user_id],
                set_=oauth_connection_on_conflict
            )
        )
        result = await self._return_from_statement(update_on_conflict_stmt)
        return self._get_entity_or_raise(result)

    async def fetch_by_google_id(self, google_id: str) -> OAuthConnection:
        stmt = (
            sa_select(OAuthConnection)
            .options(joinedload(OAuthConnection.user))
            .where(OAuthConnection.google_id == google_id)
        )
        return await self._fetch_entity(stmt)
