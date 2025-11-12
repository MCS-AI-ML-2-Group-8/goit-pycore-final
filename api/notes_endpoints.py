from fastapi import APIRouter, HTTPException
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


