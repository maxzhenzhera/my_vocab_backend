from uuid import uuid4


__all__ = ['generate_fake_refresh_token']


def generate_fake_refresh_token() -> str:
    return str(uuid4())
