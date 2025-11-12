from fastapi import APIRouter, HTTPException
from data.tag_commands import AddTag, RemoveTag
from data.note_commands import NoteCommands, CreateNote, UpdateNote
from data.note_queries import NoteQueries
from data.exceptions import NoteNotFound
from api.database import database_engine
from api.models import NoteModel
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
@router.post("")
def create_note(command: CreateNote) -> NoteModel:
    commands = NoteCommands(database_engine)
    note = commands.add_note(command)
    return mappers.map_note(note)


#  PUT /notes -> update a note by its ID
@router.put("/{note_id}")
def update_note(note_id: int, command: UpdateNote) -> NoteModel:
    try:
        commands = NoteCommands(database_engine)
        note = commands.update_note(note_id, command)
        return mappers.map_note(note)
    except NoteNotFound:
        raise HTTPException(404, {"message": "Note not found"})


# POST /notes/{note_id}/tags -> add a tag to the note
@router.post("/{note_id}/tags")
def add_tag_to_note(note_id: int, command: AddTag) -> NoteModel:
    try:
        commands = NoteCommands(database_engine)
        note = commands.add_tag_to_note(note_id, command)
        return mappers.map_note(note)
    except NoteNotFound:
        raise HTTPException(404, {"message": "Note not found"})


# DELETE /notes/{note_id} -> delete a note by its ID
@router.delete("/{note_id}")
def delete_note(note_id: int):
    commands = NoteCommands(database_engine)
    try:
        commands.delete_note(note_id)
        return {"message": "Note deleted successfully"}
    except NoteNotFound:
        raise HTTPException(404, {"message": "Note not found"})
