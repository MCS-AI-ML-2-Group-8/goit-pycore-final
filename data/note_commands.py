from sqlalchemy import select
from sqlalchemy.orm import Session
from data.abstractions import DomainCommand, DatabaseCommandHandler
from data.exceptions import ContactNotFound, NoteNotFound, TagNotFound
from data.models import Contact, Note, Tag


class CreateNote(DomainCommand):
    text: str

class UpdateNote(DomainCommand):
    text: str

class AddTag(DomainCommand):
    label: str

class RemoveTag(DomainCommand):
    label: str


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

    def delete_note(self, note_id: int) -> None:
        with Session(self.engine) as session:
            note = session.get(Note, note_id)
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

    def remove_tag_to_note(self, note_id: int, command: RemoveTag) -> None:
        with Session(self.engine) as session:
            note = session.get(Note, note_id)
            if not note:
                raise NoteNotFound()

            tag = session.scalar(select(Tag).where(Tag.label == command.label))
            if not tag:
                raise TagNotFound()

            note.tags.remove(tag)
            session.add(note)
            session.commit()
