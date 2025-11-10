from sqlalchemy import select
from sqlalchemy.orm import Session
from data.abstractions import DomainCommand, DatabaseCommandHandler
from data.exceptions import ContactNotFound, NoteNotFound, TagNotFound
from data.models import Contact, Note, Tag
from data.tag_commands import AddTag, RemoveTag


class CreateNote(DomainCommand):
    text: str

class UpdateNote(DomainCommand):
    text: str


class NoteCommands(DatabaseCommandHandler):
    def add_note_for_contact(self, contact_id: int, command: CreateNote) -> Note:
        with Session(self.engine) as session:
            contact = session.scalar(select(Contact).where(Contact.contact_id == contact_id))
            if not contact:
                raise ContactNotFound()

            note = Note()
            note.text = command.text

            contact.notes.append(note)
            session.add(note)
            session.commit()
            session.refresh(note)
            return note

    def add_note_for_contact_by_name(self, contact_name: str, command: CreateNote) -> Note:
        with Session(self.engine) as session:
            contact = session.scalar(select(Contact).where(Contact.name == contact_name))
            if not contact:
                raise ContactNotFound()

            note = Note()
            note.text = command.text

            contact.notes.append(note)
            session.add(note)
            session.commit()
            session.refresh(note)
            return note

    def add_note(self, command: CreateNote) -> Note:
        with Session(self.engine) as session:
            note = Note()
            note.text = command.text
            session.add(note)
            session.commit()
            session.refresh(note)
            return note

    def update_note(self, note_id: int, command: UpdateNote) -> Note:
        with Session(self.engine) as session:
            note = session.get(Note, note_id)
            if not note:
                raise NoteNotFound()

            note.text = command.text
            session.commit()
            session.refresh(note)
            return note

    def update_note_by_fragment(self, fragment: str, command: UpdateNote) -> Note:
        with Session(self.engine) as session:
            query = select(Note).where(Note.text.like(f"%{fragment}%"))
            note = session.scalar(query)
            if not note:
                raise NoteNotFound()

            note.text = command.text
            session.commit()
            session.refresh(note)
            return note

    def delete_note(self, note_id: int) -> None:
        with Session(self.engine) as session:
            note = session.get(Note, note_id)
            if not note:
                raise NoteNotFound()

            session.delete(note)
            session.commit()

    def delete_note_from_fragment(self, fragment: str) -> None:
        with Session(self.engine) as session:
            query = select(Note).where(Note.text.like(f"%{fragment}%"))
            note = session.scalar(query)
            if not note:
                raise NoteNotFound()

            session.delete(note)
            session.commit()

    def add_tag_to_note(self, note_id: int, command: AddTag) -> None:
        with Session(self.engine) as session:
            note = session.get(Note, note_id)
            if not note:
                raise NoteNotFound()

            tag = session.scalar(select(Tag).where(Tag.label == command.label))
            if not tag:
                tag = Tag()
                tag.label = command.label
                session.add(tag)

            if tag in note.tags:
                return # already added

            note.tags.append(tag)
            session.add(note)
            session.commit()

    def add_tag_to_note_by_fragment(self, fragment: str, command: AddTag) -> None:
        with Session(self.engine) as session:
            query = select(Note).where(Note.text.like(f"%{fragment}%"))
            note = session.scalar(query)
            if not note:
                raise NoteNotFound()

            tag = session.scalar(select(Tag).where(Tag.label == command.label))
            if not tag:
                tag = Tag()
                tag.label = command.label
                session.add(tag)

            if tag in note.tags:
                return # already added

            note.tags.append(tag)
            session.add(note)
            session.commit()

    def remove_tag_from_note(self, note_id: int, command: RemoveTag) -> None:
        with Session(self.engine) as session:
            note = session.get(Note, note_id)
            if not note:
                raise NoteNotFound()

            tag = session.scalar(select(Tag).where(
                Tag.notes.has(Note.note_id == note.note_id),
                Tag.label == command.label))

            if not tag:
                raise TagNotFound()

            note.tags.remove(tag)
            session.commit()

    def remove_tag_from_note_by_fragment(self, fragment: str, command: RemoveTag) -> None:
        with Session(self.engine) as session:
            query = select(Note).where(Note.text.like(f"%{fragment}%"))
            note = session.scalar(query)
            if not note:
                raise NoteNotFound()

            tag = session.scalar(select(Tag).where(
                Tag.notes.any(Note.note_id == note.note_id),
                Tag.label == command.label))

            if not tag:
                raise TagNotFound()

            note.tags.remove(tag)
            session.commit()
