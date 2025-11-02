from sqlalchemy import create_engine
from data.models import Base
from data.contact_commands import ContactCommands, CreateContact
from data.note_commands import CreateNote, NoteCommands, UpdateNote
from data.note_queries import NoteQueries
from data.tag_commands import AddTag, RemoveTag

engine = create_engine("sqlite:///:memory:")

Base.metadata.create_all(engine)

# Contact for notes

contact = ContactCommands(engine).add_contact(
    CreateContact(
        name="Andrii",
        phone_number="0934681185",
        date_of_birth=None
    )
)

# Notes

commands = NoteCommands(engine)
queries = NoteQueries(engine)

added_note = commands.add_note_for_contact(contact.contact_id, CreateNote(text="Hello world!"))
updated_note = commands.update_note(added_note.note_id, UpdateNote(text="Hello big world!"))

commands.add_tag_to_note(updated_note.note_id, AddTag(label="hello"))
commands.add_tag_to_note(updated_note.note_id, AddTag(label="big"))
commands.add_tag_to_note(updated_note.note_id, AddTag(label="world"))
commands.add_tag_to_note(updated_note.note_id, AddTag(label="world"))
commands.remove_tag_to_note(updated_note.note_id, RemoveTag(label="big"))

print(contact)

notes = queries.get_notes_for_contact(contact.contact_id)

print(notes)

assert notes[0].note_id == added_note.note_id

new_note = commands.add_note(CreateNote(text = "Test"))

assert new_note.note_id > 0

commands.delete_note(new_note.note_id)
