from datetime import date
from uuid import uuid4
from sqlalchemy import create_engine
from data.contact_commands import ContactAlreadyExists, ContactCommands, CreateContact, DeleteContactById, UpdateContactById
from data.models import Base

engine = create_engine("sqlite:///contacts_test.db")
contact_commands = ContactCommands(engine)
test_id = str(uuid4())

Base.metadata.create_all(engine)

def test_create_contact():
    create_contact = CreateContact(
        name=f"John Doe {test_id}",
        date_of_birth=None
    )
    contact = contact_commands.add_contact(create_contact)
    assert contact.contact_id != 0, "Contact does not have id assigned"
    assert contact.name == create_contact.name
    assert contact.date_of_birth is None

def test_create_existing_contact():
    create_contact = CreateContact(
        name="John Doe",
        date_of_birth=None
    )
    try:
        _ = contact_commands.add_contact(create_contact)
    except ContactAlreadyExists:
        pass
    else:
        assert False, "Expected exception was not raised"

def test_update_contact():
    create_contact = CreateContact(
        name=f"Jane Doe {test_id}",
        date_of_birth=None
    )
    created_contact = contact_commands.add_contact(create_contact)

    # Update
    update_contact = UpdateContactById(
        contact_id=created_contact.contact_id,
        name=f"Jane Smith {test_id}",
        date_of_birth=date(1990, 10, 27)
    )
    updated_contact = contact_commands.update_contact_by_id(update_contact)

    assert updated_contact.contact_id == created_contact.contact_id, "Contact id hasn't changed"
    assert updated_contact.name == update_contact.name
    assert updated_contact.date_of_birth is not None

def test_delete_contact():
    create_contact = CreateContact(
        name=f"Jack Black {test_id}",
        date_of_birth=None
    )
    created_contact = contact_commands.add_contact(create_contact)

    # Update
    delete_contact = DeleteContactById(
        contact_id=created_contact.contact_id
    )
    contact_commands.delete_contact_by_id(delete_contact)
