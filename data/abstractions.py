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
