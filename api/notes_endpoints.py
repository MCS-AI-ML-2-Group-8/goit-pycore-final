from fastapi import APIRouter, HTTPException
from data.tag_commands import AddTag, RemoveTag
from data.note_commands import NoteCommands, CreateNote
from data.note_queries import NoteQueries
from data.exceptions import ContactAlreadyExists
from api.database import database_engine
from api.models import ContactModel, NoteModel
import api.mappers as mappers

router = APIRouter(prefix="/notes")

# GET /notes?tag={tag} -> get all notes, and get all notes by tag
@router.get("")
def get_notes(tag: str | None = None) -> list[NoteModel]:
    queries = NoteQueries(database_engine)
    if tag is not None:
        notes = queries.get_notes_by_tag(tag)
    else:
        notes = queries.get_notes()

    return list(map(mappers.map_note, notes))

#  POST /notes -> add a note by contact ID
@router.post("/{contact_id}")
def add_note_to_contact(contact_id: int, command: CreateNote) -> NoteModel:
    commands = NoteCommands(database_engine)
    note = commands.add_note_for_contact(contact_id, command)
    
    return mappers.map_note(note)


# POST /notes/{note_id}/tags/{tag} -> add a tag to the note
@router.post("/{note_id}/tags")
def add_tag_to_note(note_id: int, command: AddTag) -> NoteModel:
    commands = NoteCommands(database_engine)
    note = commands.add_tag_to_note(note_id, command)
    # note is None here 
    return mappers.map_note(note)