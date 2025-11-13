from mcp_server.fast_mcp import FastMCP
from dotenv import load_dotenv


mcp=FastMCP()
load_dotenv()
from typing import List, Optional
from mcp_server.models import Contact, Phone, Email, Tag


# Contacts 

@mcp.tool()
def get_contacts(tag: Optional[str] = None) -> List[Contact]:
    """
    Get all contacts, optionally filtered by tag.

    Args:
        tag: Optional tag label to filter contacts

    Returns:
        List of contacts with their details (name, date_of_birth, phones, emails, tags)

    Example:
        get_contacts() - returns all contacts
        get_contacts(tag="family") - returns only contacts tagged 'family'
    """
    return get_contacts(tag)

@mcp.tool()
def get_contact(contact_id: int) -> Contact:
    """
    Get a single contact by its ID.

    Args:
        contact_id: ID of the contact to retrieve

    Returns:
        Contact details

    Example:
        get_contact(contact_id=1)
    """
    return get_contact(contact_id)

@mcp.tool()
def add_contact(name: str, date_of_birth: Optional[str] = None) -> Contact:
    """
    Create a new contact.

    Args:
        name: Name of the contact (must be unique)
        date_of_birth: Optional birth date in YYYY-MM-DD format

    Returns:
        Created contact details

    Example:
        create_contact(name="Jane Smith", date_of_birth="1990-05-15")
    """
    return add_contact(name, date_of_birth)

@mcp.tool()
def update_contact(contact_id: int, name: str, date_of_birth: Optional[str] = None) -> Contact:
    """
    Update an existing contact's details.

    Args:
        contact_id: ID of the contact to update
        name: New name of the contact
        date_of_birth: Optional new birth date in YYYY-MM-DD format

    Returns:
        Updated contact details

    Example:
        update_contact(contact_id=1, name="Jane Doe")
    """
    return update_contact(contact_id, name, date_of_birth)

@mcp.tool()
def delete_contact(contact_id: int):
    """
    Delete a contact by its ID.

    Args:
        contact_id: ID of the contact to delete

    Returns:
        None

    Example:
        delete_contact(contact_id=1)
    """
    return delete_contact(contact_id)

# Phones 

@mcp.tool()
def get_phones(contact_id: int) -> List[Phone]:
    """
    Get all phone numbers for a given contact.

    Args:
        contact_id: ID of the contact

    Returns:
        List of phone numbers

    Example:
        get_phones(contact_id=1)
    """
    return get_phones(contact_id)

@mcp.tool()
def create_phone(contact_id: int, phone_number: str) -> Phone:
    """
    Add a new phone number to a contact.

    Args:
        contact_id: ID of the contact
        phone_number: Phone number to add

    Returns:
        Created phone record

    Example:
        create_phone(contact_id=1, phone_number="+380501112233")
    """
    return create_phone(contact_id, phone_number)

@mcp.tool()
def update_phone(contact_id: int, phone_id: int, phone_number: str) -> Phone:
    """
    Update a phone number for a contact.

    Args:
        contact_id: ID of the contact
        phone_id: ID of the phone record
        phone_number: New phone number

    Returns:
        Updated phone record

    Example:
        update_phone(contact_id=1, phone_id=10, phone_number="+380501112244")
    """
    return update_phone(contact_id, phone_id, phone_number)

@mcp.tool()
def delete_phone(contact_id: int, phone_id: int):
    """
    Delete a phone number from a contact.

    Args:
        contact_id: ID of the contact
        phone_id: ID of the phone record

    Returns:
        None

    Example:
        delete_phone(contact_id=1, phone_id=10)
    """
    return delete_phone(contact_id, phone_id)
