from dataclasses import dataclass

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine
)
from sqlalchemy.orm import sessionmaker

from ..core.settings.dataclasses_.components import DBSettings


__all__ = ['DBState']


@dataclass
class DBState:
    settings: DBSettings

    def __post_init__(self) -> None:
        self.engine = create_async_engine(self.settings.sqlalchemy_url)
        self.sessionmaker = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
