from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session
from data.abstractions import DomainCommand, DatabaseCommandHandler
from data.exceptions import ContactAlreadyExists, ContactNotFound, TagNotFound
from data.models import Contact, Phone, Tag
from data.tag_commands import AddTag, RemoveTag


class CreateContact(DomainCommand):
    name: str
    phone_number: str
    date_of_birth: date | None


class UpdateContact(DomainCommand):
    name: str
    date_of_birth: date | None


class ContactCommands(DatabaseCommandHandler):
    def add_contact(self, command: CreateContact) -> Contact:
        with Session(self.engine) as session:
            duplicate = session.scalar(
                select(Contact).where(Contact.name == command.name)
            )
            if duplicate:
                raise ContactAlreadyExists()

            phone = Phone()
            phone.phone_number = command.phone_number

            contact = Contact()
            contact.name = command.name
            contact.date_of_birth = command.date_of_birth
            contact.phones.append(phone)

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

            duplicate = session.scalar(
                select(Contact).where(
                    Contact.contact_id != contact_id,
                    Contact.name == command.name
                )
            )
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

    def add_tag_to_note(self, contact_id: int, command: AddTag) -> None:
        with Session(self.engine) as session:
            contact = session.get(Contact, contact_id)
            if not contact:
                raise ContactNotFound()

            tag = session.scalar(select(Tag).where(Tag.label == command.label))
            if not tag:
                tag = Tag()
                tag.label = command.label
                session.add(tag)

            if tag in contact.tags:
                return # already added

            contact.tags.append(tag)
            session.add(contact)
            session.commit()

    def remove_tag_to_note(self, contact_id: int, command: RemoveTag) -> None:
        with Session(self.engine) as session:
            contact = session.get(Contact, contact_id)
            if not contact:
                raise ContactNotFound()

            tag = session.scalar(select(Tag).where(Tag.label == command.label))
            if not tag:
                raise TagNotFound()

            contact.tags.remove(tag)
            session.add(contact)
            session.commit()
