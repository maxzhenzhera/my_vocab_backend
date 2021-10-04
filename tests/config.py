from os import getenv

from dotenv import load_dotenv

from app.core.config.dataclasses_ import DBConfig
from app.core.config.paths import EMAIL_TEMPLATES_DIR
from fastapi_mail import ConnectionConfig as MailConnectionConfig
from app.utils.casts import to_bool


__all__ = [
    'sqlalchemy_connection_string_to_test_database',
    'mail_connection_test_config'
]


load_dotenv()


sqlalchemy_connection_string_to_test_database = DBConfig(
    getenv('TEST_DB_HOST'),
    int(getenv('TEST_DB_PORT')),
    getenv('TEST_DB_NAME'),
    getenv('TEST_DB_USER'),
    getenv('TEST_DB_PASSWORD'),
).sqlalchemy_connection_string
mail_connection_test_config = MailConnectionConfig(
    MAIL_USERNAME=getenv('TEST_MAIL_USERNAME'),
    MAIL_PASSWORD=getenv('TEST_MAIL_PASSWORD'),
    MAIL_SERVER=getenv('TEST_MAIL_SERVER'),
    MAIL_PORT=int(getenv('TEST_MAIL_PORT')),
    MAIL_FROM=getenv('TEST_MAIL_FROM'),      # noqa pydantic email validation
    MAIL_FROM_NAME=getenv('TEST_MAIL_FROM_NAME'),
    MAIL_TLS=to_bool(getenv('TEST_MAIL_TLS')),
    MAIL_SSL=to_bool(getenv('TEST_MAIL_SSL')),
    TEMPLATE_FOLDER=EMAIL_TEMPLATES_DIR,
    SUPPRESS_SEND=1
)
