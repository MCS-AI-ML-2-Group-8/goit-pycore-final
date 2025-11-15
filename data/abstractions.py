"""
Base abstractions for the data layer.

This module provides abstract base classes for database-aware components,
including query handlers, domain commands and corresponding command handlers.
"""

from pydantic import BaseModel
from sqlalchemy import Engine


class DatabaseAware:
    engine: Engine

    def __init__(self, engine: Engine):
        self.engine = engine


class DatabaseQueryHandler(DatabaseAware):
    pass


class DatabaseCommandHandler(DatabaseAware):
    pass


class DomainCommand(BaseModel):
    pass
