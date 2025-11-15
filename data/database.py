from pathlib import Path
from sqlalchemy import create_engine
from data.models import Base

database_path = Path.home() / "contacts.db"
database_engine = create_engine(f"sqlite:///{database_path.resolve()}")

Base.metadata.create_all(database_engine)
