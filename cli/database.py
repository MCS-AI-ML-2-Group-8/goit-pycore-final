from sqlalchemy import create_engine
from data.models import Base

database_engine = create_engine("sqlite:///contacts.db")

Base.metadata.create_all(database_engine)
