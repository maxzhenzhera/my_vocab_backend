from ..base import ModelWithOrmMode


__all__ = ['JWTUser']


class JWTUser(ModelWithOrmMode):
    email: str
    is_email_confirmed: bool
    is_superuser: bool
