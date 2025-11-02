from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session
from data.abstractions import DomainCommand, DatabaseCommandHandler, DomainException
from data.models import Contact


class ContactNotFound(DomainException):
    """
    Raised when contact is not found during command execution
    """

class ContactAlreadyExists(DomainException):
    """
    Raised when contact with this name already exists
    """


class CreateContact(DomainCommand):
    name: str
    date_of_birth: date | None


class UpdateContact(DomainCommand):
    name: str
    date_of_birth: date | None


class ContactCommands(DatabaseCommandHandler):
    def add_contact(self, command: CreateContact) -> Contact:
        with Session(self.engine) as session:
            duplicate = session.scalar(select(Contact).where(Contact.name == command.name))
            if duplicate:
                raise ContactAlreadyExists()

            contact = Contact()
            contact.name = command.name
            contact.date_of_birth = command.date_of_birth
            session.add(contact)
            session.commit()
            session.refresh(contact)
            session.expunge(contact)
            return contact

    def update_contact(self, contact_id: int, command: UpdateContact) -> Contact:
        with Session(self.engine) as session:
            contact = session.get(Contact, contact_id)
            if not contact:
                raise ContactNotFound()

            duplicate = session.scalar(select(Contact).where(Contact.contact_id != contact_id, Contact.name == command.name))
            if duplicate:
                raise ContactAlreadyExists()

            contact.name = command.name
            contact.date_of_birth = command.date_of_birth
            session.commit()
            session.refresh(contact)
            session.expunge(contact)
            return contact

    def delete_contact(self, contact_id: int) -> None:
        with Session(self.engine) as session:
            contact = session.get(Contact, contact_id)
            if not contact:
                raise ContactNotFound()

            session.delete(contact)
            session.commit()

    def delete_contact_by_name(self, contact_name: str) -> None:
        with Session(self.engine) as session:
            query = select(Contact).where(Contact.name == contact_name)
            contact = session.scalar(query)
            if not contact:
                raise ContactNotFound()

            session.delete(contact)
            session.commit()
