from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session
from data.abstractions import DomainCommand, DatabaseCommandHandler, DomainException
from data.models import Contact


class ContactNotFound(DomainException):
    """
    Raised when contact is not found during command execution
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
            contact = Contact()
            contact.name = command.name
            contact.date_of_birth = command.date_of_birth
            session.add(contact)
            session.commit()
            session.refresh(contact)
            return contact

    def update_contact_by_id(self, command: UpdateContactById) -> Contact:
        with Session(self.engine) as session:
            query = select(Contact).filter(Contact.contact_id == command.contact_id)
            contact = session.scalar(query)

            if not contact:
                raise ContactNotFound()

            contact.name = command.name
            contact.date_of_birth = command.date_of_birth
            session.commit()
            return contact

    def delete_contact_by_id(self, command: DeleteContactById) -> None:
        with Session(self.engine) as session:
            query = select(Contact).filter(Contact.contact_id == command.contact_id)
            contact = session.scalar(query)

            if not contact:
                raise ContactNotFound()

            session.delete(contact)
            session.commit()
