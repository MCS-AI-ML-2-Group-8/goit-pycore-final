from fastapi import APIRouter, HTTPException
from data.contact_commands import ContactCommands, CreateContact, UpdateContact
from data.contact_queries import ContactQueries
from data.note_queries import NoteQueries
from data.exceptions import ContactAlreadyExists
from api.database import database_engine
from api.models import ContactModel, NoteModel
import api.mappers as mappers

router = APIRouter(prefix="/contacts")


# GET /contacts?tag={tag} # all contacts, and all contacts by tag
@router.get("")
def get_contacts(tag: str | None = None) -> list[ContactModel]:
    queries = ContactQueries(database_engine)
    if tag is not None:
        contacts = queries.get_contacts_by_tag(tag)
    else:
        contacts = queries.get_contacts()
    return list(map(mappers.map_contact, contacts))


# GET /contacts/{contact_id} # get contact by ID
@router.get("/{contact_id}")
def get_contact(contact_id: int) -> ContactModel:
    queries = ContactQueries(database_engine)
    contact = queries.get_contact_by_id(contact_id)
    if not contact:
        raise HTTPException(404, {"message": "Contact not found"})
    return mappers.map_contact(contact)


# GET /contacts/{contact_id}/notes?tag={tag} # get contact notes, and by tag
@router.get("/{contact_id}/notes")
def get_contact_notes(contact_id: int, tag: str | None = None) -> list[NoteModel]:
    queries = NoteQueries(database_engine)
    if tag is not None:
        notes = queries.get_notes_for_contact_by_tag(contact_id, tag)
    else:
        notes = queries.get_notes_for_contact(contact_id)
    return list(map(mappers.map_note, notes))


@router.post("")
def add_contact(command: CreateContact) -> ContactModel:
    try:
        commands = ContactCommands(database_engine)
        contact = commands.add_contact(command)
        return mappers.map_contact(contact)
    except ContactAlreadyExists:
        raise HTTPException(400, {"message": "Contact already exists"})


@router.put("/{id}")
def update_contact(id: int, command: UpdateContact) -> ContactModel:
    commands = ContactCommands(database_engine)
    contact = commands.update_contact(id, command)
    return mappers.map_contact(contact)


@router.delete("/{id}")
def delete_contact(id: int) -> None:
    commands = ContactCommands(database_engine)
    commands.delete_contact(id)
