from abc import (
    ABC,
    abstractmethod
)
from dataclasses import dataclass
from typing import (
    Generic,
    Type,
    TypeVar
)

from fastapi import Depends
from sqlalchemy.engine import Result
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select as sa_select
from sqlalchemy.sql import Select

from .protocols.statements import Returnable
from ...errors import EntityDoesNotExistError
from ...models import Base
from ....api.dependencies.db import DBSessionInTransactionMarker


__all__ = [
    'SQLAlchemyModel',
    'BaseRepo'
]


SQLAlchemyModel = TypeVar('SQLAlchemyModel', bound=Base)


@dataclass  # type: ignore[misc]
class BaseRepo(ABC, Generic[SQLAlchemyModel]):
    session: AsyncSession = Depends(DBSessionInTransactionMarker)

    @property
    @abstractmethod
    def model(self) -> Type[SQLAlchemyModel]:
        """ The repository`s db entity model. """

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(model={self.model.__class__.__name__})'

    async def create_by_entity(self, entity: SQLAlchemyModel) -> SQLAlchemyModel:
        async with self.session.begin_nested():
            self.session.add(entity)
        await self.session.refresh(entity)
        return entity

    async def _return_from_statement(self, stmt: Returnable) -> Result:
        async with self.session.begin_nested():
            stmt = stmt.returning(self.model)
            orm_stmt = (
                sa_select(self.model)
                .from_statement(stmt)
                .execution_options(populate_existing=True)
            )
            result = await self.session.execute(orm_stmt)
        return result

    async def _fetch_entity(self, select_stmt: Select) -> SQLAlchemyModel:
        result = await self.session.execute(select_stmt)
        return self._get_entity_or_raise(result)

    @staticmethod
    def _get_entity_or_raise(result: Result) -> SQLAlchemyModel:
        try:
            entity = result.scalar_one()
        except NoResultFound as error:
            raise EntityDoesNotExistError from error
        else:
            return entity

    async def _fetch_entities(self, select_stmt: Select) -> list[SQLAlchemyModel]:
        result = await self.session.execute(select_stmt)
        return result.scalars().all()
