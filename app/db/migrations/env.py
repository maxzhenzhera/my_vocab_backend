import asyncio
from logging.config import fileConfig as loggingFileConfig

from alembic import context
from sqlalchemy import (
    engine_from_config,
    pool
)
from sqlalchemy.ext.asyncio import AsyncEngine

from app.core.config import get_app_settings
from app.db.models import Base


config = context.config
loggingFileConfig(config.config_file_name)

config.set_main_option('sqlalchemy.url', get_app_settings().db.sqlalchemy_url)
target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
