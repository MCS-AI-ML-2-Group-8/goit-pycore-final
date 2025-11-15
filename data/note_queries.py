"""
Query handlers for note-related database operations.

This module provides read-only database operations for notes,
including retrieval by contact, tag, and text search functionality.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session
from data.abstractions import DatabaseQueryHandler
from data.models import Contact, Note, Tag


class NoteQueries(DatabaseQueryHandler):
    def get_notes(self) -> list[Note]:
        with Session(self.engine) as session:
            query = select(Note)
            notes = session.scalars(query)
            return list(notes)

    def get_notes_for_contact(self, contact_id: int) -> list[Note]:
        with Session(self.engine) as session:
            query = select(Note).where(Note.contact.has(Contact.contact_id == contact_id))
            notes = session.scalars(query)
            return list(notes)

    def get_notes_for_contact_by_name(self, contact_name: str) -> list[Note]:
        with Session(self.engine) as session:
            query = select(Note).where(Note.contact.has(Contact.name == contact_name))
            notes = session.scalars(query)
            return list(notes)

    def get_notes_by_tag(self, tag: str) -> list[Note]:
        with Session(self.engine) as session:
            query = select(Note).join(Note.tags).where(Tag.label == tag)
            notes = session.scalars(query)
            return list(notes)

    def get_notes_for_contact_by_tag(self, contact_id: int, tag: str) -> list[Note]:
        with Session(self.engine) as session:
            query = select(Note).join(Note.tags).where(
                Note.contact.has(Contact.contact_id == contact_id),
                Tag.label == tag
            )
            notes = session.scalars(query)
            return list(notes)

    def get_notes_for_contact_by_name_and_tag(self, contact_name: str, tag: str) -> list[Note]:
        with Session(self.engine) as session:
            query = select(Note).join(Note.tags).where(
                Note.contact.has(Contact.name == contact_name),
                Tag.label == tag
            )
            notes = session.scalars(query)
            return list(notes)

    def find_note_by_text_fragment(self, text_fragment: str) -> Note | None:
        with Session(self.engine) as session:
            query = select(Note).where(Note.text.like(f"%{text_fragment}%"))
            note = session.scalar(query)
            return note
