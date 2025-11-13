from fastapi import APIRouter, HTTPException
from data.contact_commands import ContactCommands, CreateContact, UpdateContact
from data.note_commands import NoteCommands, CreateNote
from data.phone_commands import PhoneCommands, CreatePhone, UpdatePhone
from data.tag_commands import AddTag, RemoveTag
from data.contact_queries import ContactQueries
from data.note_queries import NoteQueries
from data.phone_queries import PhoneQueries
from data.email_queries import EmailQueries
from data.email_commands import EmailCommands, CreateEmail, UpdateEmail
from data.exceptions import (
    ContactAlreadyExists,
    ContactNotFound,
    TagNotFound,
    PhoneAlreadyExists,
    PhoneNotFound,
    EmailNotFound,
    EmailAlreadyExists
)
from api.database import database_engine
from api.models import ContactModel, NoteModel, PhoneModel, EmailModel
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


# POST /contacts -> Create a new contact
@router.post("")
def add_contact(command: CreateContact) -> ContactModel:
    try:
        commands = ContactCommands(database_engine)
        contact = commands.add_contact(command)
        return mappers.map_contact(contact)
    except ContactAlreadyExists:
        raise HTTPException(400, {"message": "Contact already exists"})
    except PhoneAlreadyExists:
        raise HTTPException(400, {"message": "Phone already exists"})


# POST /contacts/{contact_id}/notes -> create a not for a contact
@router.post("/{contact_id}/notes")
def add_note_to_contact(contact_id: int, command: CreateNote):
    try:
        commands = NoteCommands(database_engine)
        note = commands.add_note_for_contact(contact_id, command)
        return mappers.map_note(note)
    except ContactNotFound:
        raise HTTPException(404, {"message": "Contact not found."})


# POST /contacts/{contact_id}/tags-> add a tag for a contact
@router.post("/{contact_id}/tags")
def add_tag_to_contact(contact_id: int, command: AddTag):
    try:
        commands = ContactCommands(database_engine)
        contact = commands.add_tag_to_contact(contact_id, command)
        return mappers.map_contact(contact)
    except ContactNotFound:
        raise HTTPException(404, {"message": "Contact not found."})


# PUT /contacts/{contact_id} -> Update a contact
@router.put("/{contact_id}")
def update_contact(contact_id: int, command: UpdateContact) -> ContactModel:
    try:
        commands = ContactCommands(database_engine)
        contact = commands.update_contact(contact_id, command)
        return mappers.map_contact(contact)
    except ContactNotFound:
        raise HTTPException(404, {"message": "Contact not found."})


# DELETE /contacts/{contact_id} -> Delete a contact
@router.delete("/{contact_id}")
def delete_contact(contact_id: int) -> None:
    try:
        commands = ContactCommands(database_engine)
        commands.delete_contact(contact_id)
        return {"message": "Contact successfully deleted."}
    except ContactNotFound:
        raise HTTPException(404, {"message": "Contact not found"})


# DELETE /contacts/{contact_id}/tags -> delete tag from contact
@router.delete("/{contact_id}/tags")
def delete_tag_from_contact(contact_id: int, command: RemoveTag) -> None:
    try:
        commands = ContactCommands(database_engine)
        commands.remove_tag_from_contact(contact_id, command)
        return {"message": "Tag successfully deleted."}
    except ContactNotFound:
        raise HTTPException(404, {"message": "Contact not found"})
    except TagNotFound:
        raise HTTPException(404, {"message": "Tag not found"})


# PHOHES Endpoints

# GET /contacts/{contact_id}/phones ->  get phones by contact ID
@router.get("/{contact_id}/phones")
def get_phones_for_contact(contact_id: int) -> list[PhoneModel]:
    contact_queries = ContactQueries(database_engine)
    contact = contact_queries.get_contact_by_id(contact_id)

    if contact is None:
        raise HTTPException(404, {"message": "Contact not found"})
        
    queries = PhoneQueries(database_engine)
    phones = queries.get_contact_phones(contact_id)
    return list(map(mappers.map_phone, phones))

# POST /contacts/{contact_id}/phones -> create a phone for contact
@router.post("/{contact_id}/phones")
def create_phone(contact_id: int, command: CreatePhone):
    try:
        commands = PhoneCommands(database_engine)
        phone = commands.add_phone_for_contact(contact_id, command)
        return mappers.map_phone(phone)
    except ContactNotFound:
        raise HTTPException(404, {"message": "Contact not found."})
    except PhoneAlreadyExists:
        raise HTTPException(400, {"message": "Phone already exist."})
    
# PUT /contacts/{contact_id}/phones/{phone_id} -> update a phone for contact
@router.put("/{contact_id}/phones/{phone_id}")
def update_phone(contact_id: int, phone_id: int,  command: UpdatePhone):
    contact_queries = ContactQueries(database_engine)
    contact = contact_queries.get_contact_by_id(contact_id)

    if contact is None:
        raise HTTPException(404, {"message": "Contact not found"})
    
    try:
        commands = PhoneCommands(database_engine)
        phone = commands.update_phone(phone_id, command)
        return mappers.map_phone(phone)
    except PhoneNotFound:
        raise HTTPException(404, {"message": "Phone not found."})
    except PhoneAlreadyExists:
        raise HTTPException(400, {"message": "Phone already exist."})
    
    
# DELETE /contacts/{contact_id}/phones/{phone_id} -> Delete a phone
@router.delete("/{contact_id}/phones/{phone_id}")
def delete_phone(contact_id: int, phone_id: int) -> None:
    contact_queries = ContactQueries(database_engine)
    contact = contact_queries.get_contact_by_id(contact_id)

    if contact is None:
        raise HTTPException(404, {"message": "Contact not found"})
    
    try:
        commands = PhoneCommands(database_engine)
        commands.delete_phone(phone_id)
        return {"message": "Phone successfully deleted."}
    except PhoneNotFound:
        raise HTTPException(404, {"message": "Phone not found"})
    
    

# EMAILS Endpoints

# GET /contacts/{contact_id}/emails ->  get emails by contact ID
@router.get("/{contact_id}/emails")
def get_emails_for_contact(contact_id: int) -> list[EmailModel]:
    contact_queries = ContactQueries(database_engine)
    contact = contact_queries.get_contact_by_id(contact_id)

    if contact is None:
        raise HTTPException(404, {"message": "Contact not found"})
        
    queries = EmailQueries(database_engine)
    emails = queries.get_contact_emails(contact_id)
    return list(map(mappers.map_email, emails))

# POST /contacts/{contact_id}/emails -> create an email for contact
@router.post("/{contact_id}/emails")
def create_email(contact_id: int, command: CreateEmail) -> EmailModel:
    try:
        commands = EmailCommands(database_engine)
        email = commands.add_email_for_contact(contact_id, command)
        return mappers.map_email(email)
    except ContactNotFound:
        raise HTTPException(404, {"message": "Contact not found."})
    except EmailAlreadyExists:
        raise HTTPException(400, {"message": "Email already exists."})
    
# PUT /contacts/{contact_id}/emails/{email_id} -> update an email for contact
@router.put("/{contact_id}/emails/{email_id}")
def update_email(contact_id: int, email_id: int,  command: UpdateEmail) -> EmailModel:
    contact_queries = ContactQueries(database_engine)
    contact = contact_queries.get_contact_by_id(contact_id)

    if contact is None:
        raise HTTPException(404, {"message": "Contact not found"})
    
    try:
        commands = EmailCommands(database_engine)
        email = commands.update_email(email_id, command)
        return mappers.map_email(email)
    except EmailNotFound:
        raise HTTPException(404, {"message": "Email not found."})
    except EmailAlreadyExists:
        raise HTTPException(400, {"message": "Email already exists."})
    
# DELETE /contacts/{contact_id}/emails/{email_id} -> Delete an email
@router.delete("/{contact_id}/emails/{email_id}")
def delete_email(contact_id: int, email_id: int):
    contact_queries = ContactQueries(database_engine)
    contact = contact_queries.get_contact_by_id(contact_id)

    if contact is None:
        raise HTTPException(404, {"message": "Contact not found"})
    
    try:
        commands = EmailCommands(database_engine)
        commands.delete_email(email_id)
        return {"message": "Email successfully deleted."}
    except EmailNotFound:
        raise HTTPException(404, {"message": "Email not found"})