from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from app.core.config import settings
from app.core.database import Base

# Import models so Alembic can detect tables
from app.models.ticket import Ticket


# Alembic Config object
config = context.config


# Convert async URL -> sync URL for Alembic
database_url = settings.DATABASE_URL.replace(
    "postgresql+asyncpg",
    "postgresql+psycopg"
)

# Set database URL
config.set_main_option(
    "sqlalchemy.url",
    database_url
)


# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Metadata for autogenerate
target_metadata = Base.metadata

print("Tables:", target_metadata.tables.keys())

print(
    "Ticket columns:",
    target_metadata.tables["tickets"].columns.keys()
)

def run_migrations_offline() -> None:
    """
    Run migrations without creating DB connection
    """

    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={
            "paramstyle": "named"
        },
    )

    with context.begin_transaction():
        context.run_migrations()



def run_migrations_online() -> None:
    """
    Run migrations with DB connection
    """

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )


    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )


        with context.begin_transaction():
            context.run_migrations()



if context.is_offline_mode():
    run_migrations_offline()

else:
    run_migrations_online()