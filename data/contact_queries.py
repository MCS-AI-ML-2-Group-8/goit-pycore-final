from sqlalchemy import select
from sqlalchemy.orm import Session
from data.abstractions import DatabaseQueryHandler
from data.models import Contact, Tag


class ContactQueries(DatabaseQueryHandler):
    def get_contacts(self) -> list[Contact]:
        with Session(self.engine) as session:
            query = select(Contact)
            contacts = session.scalars(query)
            return list(contacts)

    def get_contacts_by_tag(self, tag: str) -> list[Contact]:
        with Session(self.engine) as session:
            query = select(Contact).join(Contact.tags).where(Tag.label == tag)
            contacts = session.scalars(query)
            return list(contacts)

    def get_contact_by_id(self, contact_id: int) -> Contact | None:
        with Session(self.engine) as session:
            query = select(Contact).where(Contact.contact_id == contact_id)
            contact = session.scalar(query)
            return contact

    def get_contact_by_name(self, contact_name: str) -> Contact | None:
        with Session(self.engine) as session:
            query = select(Contact).where(Contact.name == contact_name)
            contact = session.scalar(query)
            return contact
