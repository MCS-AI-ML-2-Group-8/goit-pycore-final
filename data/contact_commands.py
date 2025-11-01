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


class UpdateContactById(DomainCommand):
    contact_id: int
    name: str
    date_of_birth: date | None


class DeleteContactById(DomainCommand):
    contact_id: int


class ContactCommands(DatabaseCommandHandler):
    def add_contact(self, command: CreateContact) -> Contact:
        with Session(self.engine) as session:
            duplicate_query = select(Contact).filter(Contact.name == command.name).exists()
            duplicate_exists = session.scalar(select(duplicate_query))
            if duplicate_exists:
                raise ContactAlreadyExists()

            contact = Contact()
            contact.name = command.name
            contact.date_of_birth = command.date_of_birth
            session.add(contact)
            session.commit()
            session.refresh(contact)
            return contact

    def update_contact_by_id(self, command: UpdateContactById) -> Contact:
        with Session(self.engine) as session:
            contact = session.get(Contact, command.contact_id)

            if not contact:
                raise ContactNotFound()

            duplicate_query = select(Contact).filter(Contact.contact_id != command.contact_id, Contact.name == command.name).exists()
            duplicate_exists = session.scalar(select(duplicate_query))
            if duplicate_exists:
                raise ContactAlreadyExists()

            contact.name = command.name
            contact.date_of_birth = command.date_of_birth
            session.commit()
            session.refresh(contact)
            return contact

    def delete_contact_by_id(self, command: DeleteContactById) -> None:
        with Session(self.engine) as session:
            contact = session.get(Contact, command.contact_id)

            if not contact:
                raise ContactNotFound()

            session.delete(contact)
            session.commit()
