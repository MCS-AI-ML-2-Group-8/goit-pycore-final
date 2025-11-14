from typing import Any, List, Optional
from fastmcp import FastMCP
from datetime import date 

from api.database import database_engine as engine
from api.mappers import map_contact
from data.contact_queries import ContactQueries
from data.phone_queries import PhoneQueries
from data.note_queries import NoteQueries

mcp = FastMCP(name="Magic 8")

Data = dict[str, Any] 

def get_queries(query_type: str):
    """Returns the appropriate Queries object based on the type."""
    if query_type == "contact":
        return ContactQueries(engine)
    elif query_type == "phone":
        return PhoneQueries(engine)
    elif query_type == "note":
        return NoteQueries(engine)
    raise ValueError(f"Unknown query type: {query_type}")

# Contacts 

@mcp.tool
def get_all_contacts() -> list[Data]:
    """Retrieves a list of all contacts."""
    queries = get_queries("contact")
    contacts = queries.get_contacts()
    return [map_contact(contact).model_dump() for contact in contacts]

@mcp.tool
def get_contacts_by_tag(tag: str) -> list[Data]:
    """Retrieves a list of contacts filtered by a specific tag."""
    queries = get_queries("contact")
    contacts = queries.get_contacts_by_tag(tag)
    return [map_contact(contact).model_dump() for contact in contacts]

@mcp.tool
def get_contact_notes(contact_id: str, tag: Optional[str] = None) -> list[Data]:
    """Retrieves notes for a specific contact (by ID), optionally filtered by a tag."""
    queries = get_queries("contact")
    notes = queries.get_contact_notes(contact_id, tag)
    return [note.model_dump() for note in notes]

@mcp.tool
def create_contact(name: str, date_of_birth: Optional[date] = None) -> Data:
    """Creates a new contact with an optional date of birth."""
    queries = get_queries("contact")
    contact = queries.create_contact(name, date_of_birth)
    return contact.model_dump()

@mcp.tool
def add_note_to_contact(contact_id: str, content: str) -> Data:
    """Adds a new note to an existing contact (by ID)."""
    queries = get_queries("contact")
    note = queries.add_note_to_contact(contact_id, content)
    return note.model_dump()

@mcp.tool
def add_tag_to_contact(contact_id: str, tag: str) -> Data:
    """Adds a tag to an existing contact (by ID)."""
    queries = get_queries("contact")
    contact = queries.add_tag_to_contact(contact_id, tag)
    return contact.model_dump()

@mcp.tool
def update_contact(contact_id: str, date_of_birth: Optional[date] = None) -> Data:
    """Updates contact information (by ID), such as the date of birth."""
    queries = get_queries("contact")
    contact = queries.update_contact(contact_id, date_of_birth)
    return contact.model_dump()

@mcp.tool
def delete_contact(contact_id: str) -> Data:
    """Deletes a contact (by ID) and returns a status dictionary."""
    queries = get_queries("contact")
    queries.delete_contact(contact_id)
    return {"contact_id": contact_id, "status": "deleted"} 

# Phones 
@mcp.tool
def create_phone(name: str, number: str) -> Data:
    """Creates a new phone entry."""
    queries = get_queries("phone")
    phone = queries.create_phone(name, number)
    return phone.model_dump()

@mcp.tool
def update_phone(phone_id: int, number: str) -> Data:
    """Updates the number for an existing phone entry (by ID)."""
    queries = get_queries("phone")
    phone = queries.update_phone(phone_id, number)
    return phone.model_dump()

@mcp.tool
def delete_phone(phone_id: int) -> Data:
    """Deletes a phone entry (by ID) and returns a status dictionary."""
    queries = get_queries("phone")
    queries.delete_phone(phone_id)
    return {"phone_id": phone_id, "status": "deleted"}

# Notes 
@mcp.tool
def get_notes(tag: Optional[str] = None) -> List[Data]:
    """Retrieves a list of all notes, optionally filtered by a tag."""
    queries = get_queries("note")
    notes = queries.get_notes(tag)
    return [note.model_dump() for note in notes]

@mcp.tool
def create_note(content: str) -> Data:
    """Creates a new note."""
    queries = get_queries("note")
    note = queries.create_note(content)
    return note.model_dump()

