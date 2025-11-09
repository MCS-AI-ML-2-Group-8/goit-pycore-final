from pydantic import Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from data.abstractions import DomainCommand, DatabaseCommandHandler
from data.exceptions import ContactNotFound, EmailAlreadyExists, EmailNotFound
from data.models import Contact, Email
from data.validation import email_address_pattern


class CreateEmail(DomainCommand):
    email_address: str = Field(..., pattern=email_address_pattern)


class UpdateEmail(DomainCommand):
    email_address: str = Field(..., pattern=email_address_pattern)


class EmailCommands(DatabaseCommandHandler):
    def add_email_for_contact(self, contact_id: int, command: CreateEmail) -> Email:
        with Session(self.engine) as session:
            contact = session.scalar(select(Contact).where(Contact.contact_id == contact_id))
            if not contact:
                raise ContactNotFound()

        duplicate = session.scalar(select(Email).where(Email.email_address == command.email_address))
        if duplicate:
            raise EmailAlreadyExists()

        email = Email()
        email.email_address = command.email_address

        contact.emails.append(email)

        session.add(email)
        session.commit()
        session.refresh(email)
        session.expunge(email)
        return email

    def add_email_for_contact_by_name(self, contact_name: str, command: CreateEmail) -> Email:
        with Session(self.engine) as session:
            contact = session.scalar(select(Contact).where(Contact.name == contact_name))
            if not contact:
                raise ContactNotFound()

        duplicate = session.scalar(select(Email).where(Email.email_address == command.email_address))
        if duplicate:
            raise EmailAlreadyExists()

        email = Email()
        email.email_address = command.email_address

        contact.emails.append(email)

        session.add(email)
        session.commit()
        session.refresh(email)
        session.expunge(email)
        return email

    def update_email(self, email_id: int, command: UpdateEmail) -> Email:
        with Session(self.engine) as session:
            email = session.get(Email, email_id)
            if not email:
                raise EmailNotFound()

            duplicate = session.scalar(
                select(Email).where(
                    Email.email_id != email_id,
                    Email.email_address == command.email_address
                )
            )
            if duplicate:
                raise EmailAlreadyExists()

            email.email_address = command.email_address

            session.commit()
            session.refresh(email)
            session.expunge(email)
            return email

    def update_email_by_address(self, contact_name: str, email_address: str, command: UpdateEmail) -> Email:
        with Session(self.engine) as session:
            email = session.scalar(
                select(Email).where(
                    Email.email_address == email_address,
                    Email.contact.has(Contact.name == contact_name)
                )
            )
            if not email:
                raise EmailNotFound()

            duplicate = session.scalar(
                select(Email).where(
                    Email.email_id != email.email_id,
                    Email.email_address == command.email_address
                )
            )
            if duplicate:
                raise EmailAlreadyExists()

            email.email_address = command.email_address

            session.commit()
            session.refresh(email)
            session.expunge(email)
            return email

    def delete_email(self, email_id: int) -> None:
        with Session(self.engine) as session:
            email = session.get(Email, email_id)
            if not email:
                raise EmailNotFound()

            session.delete(email)
            session.commit()

    def delete_email_by_address(self, contact_name: str, email_address: str) -> None:
        with Session(self.engine) as session:
            email = session.scalar(
                select(Email).where(
                    Email.email_address == email_address,
                    Email.contact.has(Contact.name == contact_name)
                )
            )
            if not email:
                raise EmailNotFound()

            session.delete(email)
            session.commit()
