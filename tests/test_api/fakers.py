from uuid import uuid4


__all__ = [
    'fake_email_confirmation_token',
    'fake_refresh_token'
]


def fake_email_confirmation_token() -> str:
    return str(uuid4())


def fake_refresh_token() -> str:
    return str(uuid4())
