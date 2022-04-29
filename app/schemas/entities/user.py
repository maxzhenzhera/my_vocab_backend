from datetime import datetime

from pydantic import (
    BaseModel,
    EmailStr
)

from ..base import (
    IDModelMixin,
    ModelWithOrmMode
)


__all__ = [
    'UserInCreate',
    'UserInLogin',
    'UserInUpdate',
    'UserInResponse'
]


class UserInCreate(BaseModel):
    email: EmailStr
    password: str


class UserInLogin(UserInCreate):
    pass


class UserInUpdate(BaseModel):
    email: EmailStr | None
    password: str | None


class UserInResponse(IDModelMixin, ModelWithOrmMode):
    email: EmailStr
    email_confirmation_token: str
    is_active: bool
    is_email_confirmed: bool
    is_superuser: bool
    email_confirmed_at: datetime | None
