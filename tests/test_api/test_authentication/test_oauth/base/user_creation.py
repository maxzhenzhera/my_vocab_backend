from abc import ABC
from datetime import timedelta

from app.db.models import User
from ...base import BaseTestUserCreationRouteCase
from .....utils.datetime_ import assert_datetime


__all__ = ['BaseTestOAuthUserCreationRouteCase']


class BaseTestOAuthUserCreationRouteCase(
    BaseTestUserCreationRouteCase,
    ABC
):
    def _test_created_user_claims(self, user: User):
        assert user.is_email_confirmed
        assert_datetime(
            actual=user.email_confirmed_at,
            delta=timedelta(seconds=5)
        )
