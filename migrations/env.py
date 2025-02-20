import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine

from app.auth.infrastructure.persistence.models.user import User  # noqa: F401
from app.character.infrastructure.persistence.models.character import (  # noqa: F401
    Character,
)
from app.core.infrastructure.persistence.models.base import BaseModel
from app.core.settings.config import settings
from app.scenario.infrastructure.persistence.models.scenario import (
    Scenario,  # noqa: F401
)

print(settings.DB_NAME)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", settings.get_database_url())

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Dynamically import all models
# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None

target_metadata = [BaseModel.metadata]

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


# def run_migrations_offline() -> None:
#     """Run migrations in 'offline' mode.

#     This configures the context with just a URL
#     and not an Engine, though an Engine is acceptable
#     here as well.  By skipping the Engine creation
#     we don't even need a DBAPI to be available.

#     Calls to context.execute() here emit the given string to the
#     script output.

#     """
#     context.configure(
#         url=config.get_main_option("sqlalchemy.url"),
#         target_metadata=target_metadata,
#         literal_binds=True,
#     )
#     with context.begin_transaction():
#         context.run_migrations()


# def run_migrations_online() -> None:
#     """Run migrations in 'online' mode.

#     In this scenario we need to create an Engine
#     and associate a connection with the context.

#     """
#     connectable = engine_from_config(
#         config.get_section(config.config_ini_section),  # type: ignore
#         prefix="sqlalchemy.",
#         poolclass=pool.NullPool,
#     )
#     with connectable.connect() as connection:
#         context.configure(connection=connection, target_metadata=target_metadata)
#         with context.begin_transaction():
#             context.run_migrations()


# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     run_migrations_online()


def run_migrations_online():
    connectable = context.config.attributes.get("connection", None)
    if connectable is None:
        connectable = AsyncEngine(
            engine_from_config(
                context.config.get_section(context.config.config_ini_section),  # type: ignore
                prefix="sqlalchemy.",
                poolclass=pool.NullPool,
                future=True,
            )
        )

    if isinstance(connectable, AsyncEngine):
        asyncio.run(run_async_migrations(connectable))
    else:
        do_run_migrations(connectable)


async def run_async_migrations(connectable):
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


run_migrations_online()

run_migrations_online()
