"""
Database initialization and configuration.

This module sets up the SQLite database connection and creates all tables.
The database location can be configured via the Magic_DB_PATH environment variable (for deployment),
otherwise it defaults to the user's home directory.
"""

import os
from pathlib import Path
from sqlalchemy import create_engine
from data.models import Base

configured_path = os.getenv("Magic_DB_PATH")
configured_name = "contacts.db"

database_path = Path(configured_path) / configured_name if configured_path else Path.home() / configured_name
database_engine = create_engine(f"sqlite:///{database_path.resolve()}")

Base.metadata.create_all(database_engine)
