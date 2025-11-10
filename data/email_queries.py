from sqlalchemy import select
from sqlalchemy.orm import Session
from data.abstractions import DatabaseQueryHandler
from data.models import Contact, Email


class EmailQueries(DatabaseQueryHandler):
    def get_contact_emails(self, contact_id: int) -> list[Email]:
        with Session(self.engine) as session:
            query = select(Email).where(Email.contact_id == contact_id)
            emails = session.scalars(query)
            return list(emails)

    def get_contact_emails_by_name(self, contact_name: str) -> list[Email]:
        with Session(self.engine) as session:
            query = select(Email).where(Email.contact.has(Contact.name == contact_name))
            emails = session.scalars(query)
            return list(emails)
