from os import getenv

from dotenv import load_dotenv

from app.core.config import DBConfig    # noqa


__all__ = ['sqlalchemy_connection_string_to_test_database']


load_dotenv()


sqlalchemy_connection_string_to_test_database = DBConfig(
    getenv('TEST_DB_HOST'),
    int(getenv('TEST_DB_PORT')),
    getenv('TEST_DB_NAME'),
    getenv('TEST_DB_USER'),
    getenv('TEST_DB_PASSWORD'),
).sqlalchemy_connection_string
