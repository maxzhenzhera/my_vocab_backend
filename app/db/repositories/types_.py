from typing import TypeVar

from pydantic import BaseModel

from ..models import Base


__all__ = [
    'ModelType',
    'CreateSchemaType',
    'UpdateSchemaType'
]


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)
