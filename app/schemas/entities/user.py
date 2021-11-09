from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    EmailStr
)

from ..base import (
    IDModelMixin,
    ModelWithOrmMode
)


__all__ = [
    'UserBaseInCreate',
    'UserInCreate',
    'UserInLogin',
    'UserInUpdate',
    'UserInResponse'
]


class UserBaseInCreate(BaseModel):
    email: EmailStr


class UserInCreate(UserBaseInCreate):
    password: str


class UserInLogin(UserInCreate):
    pass


class UserInUpdate(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]


class UserInResponse(IDModelMixin, ModelWithOrmMode):
    email: EmailStr
    email_confirmation_link: str
    is_active: bool
    is_email_confirmed: bool
    is_superuser: bool
    email_confirmed_at: Optional[datetime]