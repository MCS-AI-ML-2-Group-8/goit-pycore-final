"""
Query handlers for phone number-related database operations.

This module provides read-only database operations for retrieving
phone numbers associated with contacts.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session
from data.abstractions import DatabaseQueryHandler
from data.models import Contact, Phone


class PhoneQueries(DatabaseQueryHandler):
    def get_contact_phones(self, contact_id: int) -> list[Phone]:
        with Session(self.engine) as session:
            query = select(Phone).where(Phone.contact_id == contact_id)
            phones = session.scalars(query)
            return list(phones)

    def get_contact_phones_by_name(self, contact_name: str) -> list[Phone]:
        with Session(self.engine) as session:
            query = select(Phone).where(Phone.contact.has(Contact.name == contact_name))
            phones = session.scalars(query)
            return list(phones)
