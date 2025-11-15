from typing import Any
from fastmcp import FastMCP
from datetime import date
from data.contact_commands import ContactCommands, CreateContact, UpdateContact
from data.contact_queries import ContactQueries
from data.models import BirthdayReminder
from data.phone_commands import PhoneCommands, CreatePhone, UpdatePhone
from data.phone_queries import PhoneQueries
from data.email_commands import EmailCommands, CreateEmail, UpdateEmail
from data.email_queries import EmailQueries
from data.note_commands import NoteCommands, CreateNote, UpdateNote
from data.note_queries import NoteQueries
from data.tag_commands import AddTag, RemoveTag
from data.database import database_engine as engine
from api.mappers import map_contact, map_note, map_phone, map_email

mcp = FastMCP(name="Magic 8")

Data = dict[str, Any]

# Contacts

@mcp.tool
def get_all_contacts() -> list[Data]:
    """Retrieves a list of all contacts."""
    queries = ContactQueries(engine)
    contacts = queries.get_contacts()
    return [map_contact(contact).model_dump() for contact in contacts]

@mcp.tool
def get_contact_by_name(contact_name: str) -> Data | None:
    """Retrieves a single contact by name."""
    queries = ContactQueries(engine)
    contact = queries.get_contact_by_name(contact_name)
    return map_contact(contact).model_dump() if contact else None

@mcp.tool
def get_contacts_by_tag(tag: str) -> list[Data]:
    """Retrieves a list of contacts filtered by a specific tag."""
    queries = ContactQueries(engine)
    contacts = queries.get_contacts_by_tag(tag)
    return [map_contact(contact).model_dump() for contact in contacts]

def _map_reminder(reminder: BirthdayReminder):
    return {
        "contact": map_contact(reminder.contact).model_dump(),
        "celebration_date": reminder.bidthday.isoformat()
    }

@mcp.tool
def get_upcoming_birthdays(days: int = 7) -> list[Data]:
    """Retrieves contacts with birthdays in the next N days (default 7)."""
    queries = ContactQueries(engine)
    reminders = queries.get_contacts_with_birthdays_in_days(days)
    return [_map_reminder(r) for r in reminders]

@mcp.tool
def get_contact_notes(contact_name: str, tag: str | None = None) -> list[Data]:
    """Retrieves notes for a contact by name, optionally filtered by a tag."""
    queries = NoteQueries(engine)
    if tag:
        notes = queries.get_notes_for_contact_by_name_and_tag(contact_name, tag)
    else:
        notes = queries.get_notes_for_contact_by_name(contact_name)
    return [map_note(note).model_dump() for note in notes]

@mcp.tool
def create_contact(name: str, phone_number: str, date_of_birth: date | None = None) -> Data:
    """Creates a new contact with an optional date of birth."""
    commands = ContactCommands(engine)
    contact = commands.add_contact(
        CreateContact(
            name=name,
            phone_number=phone_number,
            date_of_birth=date_of_birth
        )
    )
    return map_contact(contact).model_dump()

@mcp.tool
def add_note_to_contact(contact_name: str, content: str) -> Data:
    """Adds a new note to an existing contact by name."""
    commands = NoteCommands(engine)
    note = commands.add_note_for_contact_by_name(contact_name, CreateNote(text=content))
    return map_note(note).model_dump()

@mcp.tool
def add_tag_to_contact(contact_name: str, tag: str) -> Data:
    """Adds a tag to an existing contact by name."""
    commands = ContactCommands(engine)
    commands.add_tag_to_contact_by_name(contact_name, AddTag(label=tag))
    return {"contact_name": contact_name, "tag": tag, "status": "added"}

@mcp.tool
def remove_tag_from_contact(contact_name: str, tag: str) -> Data:
    """Removes a tag from an existing contact by name."""
    commands = ContactCommands(engine)
    commands.remove_tag_from_contact_by_name(contact_name, RemoveTag(label=tag))
    return {"contact_name": contact_name, "tag": tag, "status": "removed"}

@mcp.tool
def update_contact(contact_name: str, new_name: str, date_of_birth: date | None = None) -> Data:
    """Updates contact information by name, including the name itself and date of birth."""
    commands = ContactCommands(engine)
    contact = commands.update_contact_by_name(contact_name, UpdateContact(name=new_name, date_of_birth=date_of_birth))
    return map_contact(contact).model_dump()

@mcp.tool
def delete_contact(contact_name: str) -> Data:
    """Deletes a contact by name and returns a status dictionary."""
    commands = ContactCommands(engine)
    commands.delete_contact_by_name(contact_name)
    return {"contact_name": contact_name, "status": "deleted"}

# Phones
@mcp.tool
def get_contact_phones(contact_name: str) -> list[Data]:
    """Retrieves all phone numbers for a contact by name."""
    queries = PhoneQueries(engine)
    phones = queries.get_contact_phones_by_name(contact_name)
    return [map_phone(phone).model_dump() for phone in phones]

@mcp.tool
def create_phone(contact_name: str, phone_number: str) -> Data:
    """Creates a new phone entry for a contact by name."""
    commands = PhoneCommands(engine)
    phone = commands.add_phone_for_contact_by_name(contact_name, CreatePhone(phone_number=phone_number))
    return map_phone(phone).model_dump()

@mcp.tool
def update_phone(contact_name: str, old_phone_number: str, new_phone_number: str) -> Data:
    """Updates the phone number for a contact by name and old phone number."""
    commands = PhoneCommands(engine)
    phone = commands.update_phone_by_number(contact_name, old_phone_number, UpdatePhone(phone_number=new_phone_number))
    return map_phone(phone).model_dump()

@mcp.tool
def delete_phone(contact_name: str, phone_number: str) -> Data:
    """Deletes a phone entry for a contact by name and phone number."""
    commands = PhoneCommands(engine)
    commands.delete_phone_by_number(contact_name, phone_number)
    return {"contact_name": contact_name, "phone_number": phone_number, "status": "deleted"}

# Emails
@mcp.tool
def get_contact_emails(contact_name: str) -> list[Data]:
    """Retrieves all email addresses for a contact by name."""
    queries = EmailQueries(engine)
    emails = queries.get_contact_emails_by_name(contact_name)
    return [map_email(email).model_dump() for email in emails]

@mcp.tool
def create_email(contact_name: str, email_address: str) -> Data:
    """Creates a new email entry for a contact by name."""
    commands = EmailCommands(engine)
    email = commands.add_email_for_contact_by_name(contact_name, CreateEmail(email_address=email_address))
    return map_email(email).model_dump()

@mcp.tool
def update_email(contact_name: str, old_email_address: str, new_email_address: str) -> Data:
    """Updates the email address for a contact by name and old email address."""
    commands = EmailCommands(engine)
    email = commands.update_email_by_address(contact_name, old_email_address, UpdateEmail(email_address=new_email_address))
    return map_email(email).model_dump()

@mcp.tool
def delete_email(contact_name: str, email_address: str) -> Data:
    """Deletes an email entry for a contact by name and email address."""
    commands = EmailCommands(engine)
    commands.delete_email_by_address(contact_name, email_address)
    return {"contact_name": contact_name, "email_address": email_address, "status": "deleted"}

# Notes
@mcp.tool
def get_notes(tag: str | None = None) -> list[Data]:
    """Retrieves a list of all notes, optionally filtered by a tag."""
    queries = NoteQueries(engine)
    if tag:
        notes = queries.get_notes_by_tag(tag)
    else:
        notes = queries.get_notes()
    return [map_note(note).model_dump() for note in notes]

@mcp.tool
def find_note_by_text(text_fragment: str) -> Data | None:
    """Finds a note by searching for a text fragment."""
    queries = NoteQueries(engine)
    note = queries.find_note_by_text_fragment(text_fragment)
    return map_note(note).model_dump() if note else None

@mcp.tool
def create_note(content: str) -> Data:
    """Creates a new note."""
    commands = NoteCommands(engine)
    note = commands.add_note(CreateNote(text=content))
    return map_note(note).model_dump()

@mcp.tool
def update_note_by_text(text_fragment: str, new_content: str) -> Data:
    """Updates a note by finding it with a text fragment."""
    commands = NoteCommands(engine)
    note = commands.update_note_by_fragment(text_fragment, UpdateNote(text=new_content))
    return map_note(note).model_dump()

@mcp.tool
def delete_note_by_text(text_fragment: str) -> Data:
    """Deletes a note by finding it with a text fragment."""
    commands = NoteCommands(engine)
    commands.delete_note_from_fragment(text_fragment)
    return {"text_fragment": text_fragment, "status": "deleted"}

@mcp.tool
def add_tag_to_note_by_text(text_fragment: str, tag: str) -> Data:
    """Adds a tag to a note by finding it with a text fragment."""
    commands = NoteCommands(engine)
    commands.add_tag_to_note_by_fragment(text_fragment, AddTag(label=tag))
    return {"text_fragment": text_fragment, "tag": tag, "status": "added"}

@mcp.tool
def remove_tag_from_note_by_text(text_fragment: str, tag: str) -> Data:
    """Removes a tag from a note by finding it with a text fragment."""
    commands = NoteCommands(engine)
    commands.remove_tag_from_note_by_fragment(text_fragment, RemoveTag(label=tag))
    return {"text_fragment": text_fragment, "tag": tag, "status": "removed"}
