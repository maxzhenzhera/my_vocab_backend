from abc import ABC

from sqlalchemy import (
    delete as sa_delete,
    update as sa_update,
)
from sqlalchemy.future import select as sa_select

from .base import BaseRepository
from .types_ import (
    ModelType,
    UpdateSchemaType
)


__all__ = ['BaseCRUDRepository']


class BaseCRUDRepository(BaseRepository, ABC):
    """
    Complement the base repository with essentials CRUD operations.

    TODO: https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app/crud/crud_item.py
    """

    async def fetch_by_id(self, id_: int) -> ModelType:
        stmt = (
            sa_select(self.model)
            .where(self.model.id == id_)
        )
        return await self._fetch_entity(stmt)

    async def fetch_all(self) -> list[ModelType]:
        stmt = sa_select(self.model)
        return await self._fetch_entities(stmt)

    async def fetch_with_limit_and_offset(self, limit: int, offset: int) -> list[ModelType]:
        stmt = (
            sa_select(self.model)
            .limit(limit)
            .offset(offset)
        )
        return await self._fetch_entities(stmt)

    async def update_by_id(self, id_: int, schema_in_update: UpdateSchemaType) -> ModelType:
        update_data = self._exclude_unset_from_schema(schema_in_update)
        stmt = (
            sa_update(self.model)
            .where(self.model.id == id_)
            .values(**update_data)
        )
        return await self._return_from_statement(stmt)

    async def delete_by_id(self, id_: int) -> ModelType:
        stmt = (
            sa_delete(self.model)
            .where(self.model.id == id_)
        )
        return await self._return_from_statement(stmt)
