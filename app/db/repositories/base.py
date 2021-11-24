from abc import (
    ABC,
    abstractmethod
)
from typing import (
    Type,
    Union
)

from sqlalchemy.engine import Result
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select as sa_select
from sqlalchemy.sql import (
    Delete,
    Insert,
    Update,
    Select
)

from .types_ import (
    ModelType,
    CreateSchemaType,
    UpdateSchemaType
)
from ..errors import EntityDoesNotExistError


__all__ = ['BaseRepository']


class BaseRepository(ABC):
    """
    Implements a base repository to create a particular repository for corresponded model.
    Each child class must override class attribute about model that related to:

        .. attribute:: model: Type[ModelType]
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @property
    @abstractmethod
    def model(self) -> Type[ModelType]:
        """
        The repository`s db entity model.

        Abstract *class* attribute:
            model: ClassVar[ModelType] = Model
        """

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(model={self.model.__cls__.__name__})'

    async def create_by_schema(self, schema_in_create: CreateSchemaType) -> ModelType:
        return await self.create_by_entity(self.model(**schema_in_create.dict()))

    async def create_by_entity(self, entity: ModelType) -> ModelType:
        async with self.session.begin_nested():
            self.session.add(entity)
        await self.session.refresh(entity)
        return entity

    @staticmethod
    def _exclude_unset_from_schema(schema_in_update: UpdateSchemaType) -> dict:
        return schema_in_update.dict(exclude_unset=True)

    async def _return_from_statement(self, statement: Union[Update, Insert, Delete]) -> ModelType:
        async with self.session.begin_nested():
            stmt = statement.returning(self.model)
            orm_stmt = (
                sa_select(self.model)
                .from_statement(stmt)
                .execution_options(populate_existing=True)
            )
            result: Result = await self.session.execute(orm_stmt)
        return result.scalar()

    async def _fetch_entity(self, select_statement: Select) -> ModelType:
        result: Result = await self.session.execute(select_statement)
        return self._get_entity_or_raise(result)

    @staticmethod
    def _get_entity_or_raise(result: Result) -> ModelType:
        try:
            entity = result.scalar_one()
        except NoResultFound:
            raise EntityDoesNotExistError
        else:
            return entity

    async def _fetch_entities(self, select_statement: Select) -> list[ModelType]:
        result: Result = await self.session.execute(select_statement)
        return result.scalars().all()
