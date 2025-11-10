from fastapi import APIRouter, HTTPException
from data.contact_commands import ContactCommands, CreateContact, UpdateContact
from data.contact_queries import ContactQueries
from data.exceptions import ContactAlreadyExists
from api.database import database_engine
from api.models import ContactModel
import api.mappers as mappers

router = APIRouter(prefix="/contacts")

@router.get("")
def get_contacts(tag: str | None = None) -> list[ContactModel]:
    queries = ContactQueries(database_engine)
    if tag is not None:
        contacts = queries.get_contacts_by_tag(tag)
    else:
        contacts = queries.get_contacts()

    return list(map(mappers.map_contact, contacts))

@router.post("")
def add_contact(command: CreateContact) -> ContactModel:
    try:
        commands = ContactCommands(database_engine)
        contact = commands.add_contact(command)
        return mappers.map_contact(contact)
    except ContactAlreadyExists:
        raise HTTPException(400, { "message": "Contact already exists" })

@router.put("/{id}")
def update_contact(id: int, command: UpdateContact) -> ContactModel:
    commands = ContactCommands(database_engine)
    contact = commands.update_contact(id, command)
    return mappers.map_contact(contact)

@router.delete("/{id}")
def delete_contact(id: int) -> None:
    commands = ContactCommands(database_engine)
    commands.delete_contact(id)
