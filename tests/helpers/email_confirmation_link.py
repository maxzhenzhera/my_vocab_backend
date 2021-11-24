from uuid import uuid4


__all__ = ['generate_fake_email_confirmation_link']


def generate_fake_email_confirmation_link() -> str:
    return str(uuid4())
