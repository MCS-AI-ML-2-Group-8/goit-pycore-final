from sqlalchemy import select
from sqlalchemy.orm import Session
from data.abstractions import DomainCommand, DatabaseCommandHandler
from data.exceptions import ContactNotFound, PhoneAlreadyExists, PhoneNotFound
from data.models import Contact, Phone


class CreatePhone(DomainCommand):
    phone_number: str


class UpdatePhone(DomainCommand):
    phone_number: str


class PhoneCommands(DatabaseCommandHandler):
    def add_phone_for_contact(self, contact_id: int, command: CreatePhone) -> Phone:
        with Session(self.engine) as session:
            contact = session.scalar(select(Contact).where(Contact.contact_id == contact_id))
            if not contact:
                raise ContactNotFound()

        duplicate = session.scalar(select(Phone).where(Phone.phone_number == command.phone_number))
        if duplicate:
            raise PhoneAlreadyExists()

        phone = Phone()
        phone.phone_number = command.phone_number

        contact.phones.append(phone)

        session.add(phone)
        session.commit()
        session.refresh(phone)
        session.expunge(phone)
        return phone

    def add_phone_for_contact_by_name(self, contact_name: str, command: CreatePhone) -> Phone:
        with Session(self.engine) as session:
            contact = session.scalar(select(Contact).where(Contact.name == contact_name))
            if not contact:
                raise ContactNotFound()

        duplicate = session.scalar(select(Phone).where(Phone.phone_number == command.phone_number))
        if duplicate:
            raise PhoneAlreadyExists()

        phone = Phone()
        phone.phone_number = command.phone_number

        contact.phones.append(phone)

        session.add(phone)
        session.commit()
        session.refresh(phone)
        session.expunge(phone)
        return phone

    def update_phone(self, phone_id: int, command: UpdatePhone) -> Phone:
        with Session(self.engine) as session:
            phone = session.get(Phone, phone_id)
            if not phone:
                raise PhoneNotFound()

            duplicate = session.scalar(
                select(Phone).where(
                    Phone.phone_id != phone_id,
                    Phone.phone_number == command.phone_number
                )
            )
            if duplicate:
                raise PhoneAlreadyExists()

            phone.phone_number = command.phone_number

            session.commit()
            session.refresh(phone)
            session.expunge(phone)
            return phone

    def update_phone_by_number(self, contact_name: str, phone_number: str, command: UpdatePhone) -> Phone:
        with Session(self.engine) as session:
            phone = session.scalar(
                select(Phone).where(
                    Phone.phone_number == phone_number,
                    Phone.contact.has(Contact.name == contact_name)
                )
            )
            if not phone:
                raise PhoneNotFound()

            duplicate = session.scalar(
                select(Phone).where(
                    Phone.phone_id != phone.phone_id,
                    Phone.phone_number == command.phone_number
                )
            )
            if duplicate:
                raise PhoneAlreadyExists()

            phone.phone_number = command.phone_number

            session.commit()
            session.refresh(phone)
            session.expunge(phone)
            return phone

    def delete_phone(self, phone_id: int) -> None:
        with Session(self.engine) as session:
            phone = session.get(Phone, phone_id)
            if not phone:
                raise PhoneNotFound()

            session.delete(phone)
            session.commit()

    def delete_phone_by_number(self, contact_name: str, phone_number: str) -> None:
        with Session(self.engine) as session:
            phone = session.scalar(
                select(Phone).where(
                    Phone.phone_number == phone_number,
                    Phone.contact.has(Contact.name == contact_name)
                )
            )
            if not phone:
                raise PhoneNotFound()

            session.delete(phone)
            session.commit()
