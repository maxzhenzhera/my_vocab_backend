from pydantic import (
    BaseConfig,
    BaseModel
)


__all__ = [
    'IDModelMixin',
    'ModelWithOrmMode'
]


class IDModelMixin(BaseModel):
    id: int


class ModelWithOrmMode(BaseModel):
    class Config(BaseConfig):
        orm_mode = True
