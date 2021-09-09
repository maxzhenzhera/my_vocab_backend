import abc
from typing import Type

from sqlalchemy import (
    delete as sa_delete,
    update as sa_update,
)
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select as sa_select

from ._types import (
    ModelType,
    CreateSchemaType,
    UpdateSchemaType
)


__all__ = ['BaseRepository']


class BaseRepository(abc.ABC):
    """
    Implements a base repository to create a particular repository for corresponded model.
    Each child class must override class attribute about model that related to:

        .. attribute:: model: Type[ModelType]
    """

    model: Type[ModelType]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def session(self) -> AsyncSession:
        return self._session

    async def create_by_schema(self, schema_in_create: CreateSchemaType) -> ModelType:
        return await self.create_by_entity(self.model(**schema_in_create.dict()))

    async def create_by_entity(self, entity: ModelType) -> ModelType:
        async with self._session.begin_nested():
            self._session.add(entity)
        await self._session.refresh(entity)
        return entity

    async def fetch_by_id(self, id_: int) -> ModelType:
        stmt = sa_select(self.model).where(self.model.id == id_)
        result: Result = await self._session.execute(stmt)
        return result.scalar()

    async def update_by_id(self, id_: int, schema_in_update: UpdateSchemaType) -> ModelType:
        update_data = schema_in_update.dict(exclude_unset=True)
        async with self._session.begin_nested():
            stmt = sa_update(self.model).where(self.model.id == id_).values(**update_data).returning(self.model)
            orm_stmt = sa_select(self.model).from_statement(stmt).execution_options(populate_existing=True)
            result: Result = await self._session.execute(orm_stmt)
        return result.scalar()

    async def delete_by_id(self, id_: int) -> None:
        async with self._session.begin_nested():
            stmt = sa_delete(self.model).where(self.model.id == id_)
            await self._session.execute(stmt)
