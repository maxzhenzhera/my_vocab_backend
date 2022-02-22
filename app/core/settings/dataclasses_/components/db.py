from dataclasses import (
    InitVar,
    dataclass
)
from typing import ClassVar


__all__ = ['DBSettings']


@dataclass
class DBSettings:
    dialect: ClassVar[str] = 'postgresql'
    driver: ClassVar[str] = 'asyncpg'

    uri: InitVar[str]

    def __post_init__(self, uri: str) -> None:
        self.sqlalchemy_url = uri.replace(
            self.dialect,
            f'{self.dialect}+{self.driver}'
        )
