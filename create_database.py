from sqlalchemy import create_engine
from data.models import Base

engine = create_engine("sqlite:///contacts.db")

Base.metadata.create_all(engine)
