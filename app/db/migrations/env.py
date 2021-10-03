import asyncio
import sys
from logging.config import fileConfig as loggingFileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine

# import from local project ------------------------------------------------------------------------------------------
sys.path.append(str(Path(__file__).parents[3]))

from app.core.config.config import sqlalchemy_connection_string     # noqa E402 module level import not at top of file
from app.db.models import Base                                      # noqa E402 module level import not at top of file
# --------------------------------------------------------------------------------------------------------------------


config = context.config
loggingFileConfig(config.config_file_name)

config.set_main_option('sqlalchemy.url', sqlalchemy_connection_string)
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
