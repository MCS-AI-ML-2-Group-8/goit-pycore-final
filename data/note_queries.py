from sqlalchemy import select
from sqlalchemy.orm import Session
from data.abstractions import DatabaseQueryHandler
from data.models import Contact, Note


class NoteQueries(DatabaseQueryHandler):
    def get_notes_for_contact(self, contact_id: int) -> list[Note]:
        with Session(self.engine) as session:
            query = select(Note).where(Note.contact.has(Contact.contact_id == contact_id))
            notes = session.scalars(query)
            return list(notes)
