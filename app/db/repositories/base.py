import abc
from typing import (
    Type,
    Union
)

from sqlalchemy import (
    delete as sa_delete,
    update as sa_update,
)
from sqlalchemy.engine import Result
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select as sa_select
from sqlalchemy.sql import (
    Select,
    Update,
    Delete
)

from ._types import (
    ModelType,
    CreateSchemaType,
    UpdateSchemaType
)
from ..errors import EntityDoesNotExistError


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

    async def update(self, id_: int, schema_in_update: UpdateSchemaType) -> ModelType:
        update_data = self._exclude_unset_from_schema(schema_in_update)
        stmt = sa_update(self.model).where(self.model.id == id_).values(**update_data)
        return await self._return_from_statement(stmt)

    @staticmethod
    def _exclude_unset_from_schema(schema_in_update: UpdateSchemaType) -> dict:
        return schema_in_update.dict(exclude_unset=True)

    async def delete_by_id(self, id_: int) -> ModelType:
        stmt = sa_delete(self.model).where(self.model.id == id_)
        return await self._return_from_statement(stmt)

    async def _return_from_statement(self, statement: Union[Update, Delete]) -> ModelType:
        async with self._session.begin_nested():
            stmt = statement.returning(self.model)
            orm_stmt = sa_select(self.model).from_statement(stmt).execution_options(populate_existing=True)
            result: Result = await self._session.execute(orm_stmt)
        return result.scalar()

    async def fetch_by_id(self, id_: int) -> ModelType:
        stmt = sa_select(self.model).where(self.model.id == id_)
        return await self._fetch_entity(stmt)

    async def _fetch_entity(self, select_statement: Select) -> ModelType:
        result: Result = await self._session.execute(select_statement)
        return self._get_entity_or_raise(result)

    @staticmethod
    def _get_entity_or_raise(result: Result) -> ModelType:
        try:
            entity = result.scalar_one()
        except NoResultFound:
            raise EntityDoesNotExistError
        else:
            return entity

    async def fetch_all(self) -> list[ModelType]:
        stmt = sa_select(self.model)
        return await self._fetch_entities(stmt)

    async def fetch_with_limit_and_offset(self, limit: int, offset: int) -> list[ModelType]:
        stmt = sa_select(self.model).limit(limit).offset(offset)
        return await self._fetch_entities(stmt)

    async def _fetch_entities(self, select_statement: Select) -> list[ModelType]:
        result: Result = await self._session.execute(select_statement)
        return result.scalars().all()
