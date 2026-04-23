"""Compatibility shim for the database configuration.

The original root-level Alembic environment file shadowed the installed
`alembic` package and raised an import error on startup. Keeping this module
lightweight avoids that collision while still exposing the database URL for
any local tooling that imports it.
"""

from database import Base, SQLALCHEMY_DATABASE_URL


DATABASE_URL = SQLALCHEMY_DATABASE_URL
target_metadata = Base.metadata