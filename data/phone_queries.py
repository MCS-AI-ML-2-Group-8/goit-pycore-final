from sqlalchemy import select
from sqlalchemy.orm import Session
from data.abstractions import DatabaseQueryHandler
from data.models import Phone


class PhoneQueries(DatabaseQueryHandler):
    def get_contact_phones(self, contact_id: int) -> list[Phone]:
        with Session(self.engine) as session:
            query = select(Phone).where(Phone.contact_id == contact_id)
            phones = session.scalars(query)
            return list(phones)
