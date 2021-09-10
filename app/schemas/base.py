from pydantic import (
    BaseConfig,
    BaseModel
)


__all__ = ['ModelWithOrmMode']


class ModelWithOrmMode(BaseModel):
    class Config(BaseConfig):
        orm_mode = True
