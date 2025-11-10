from datetime import date
from sqlalchemy import create_engine
from data.contact_commands import ContactCommands, CreateContact, UpdateContact
from data.exceptions import ContactAlreadyExists
from data.models import Base

engine = create_engine("sqlite:///:memory:")
commands = ContactCommands(engine)

Base.metadata.create_all(engine)

def test_create_contact():
    create_contact = CreateContact(
        name="John Doe",
        date_of_birth=None,
        phone_number="0001112223"
    )
    contact = commands.add_contact(create_contact)
    assert contact.contact_id != 0, "Contact does not have id assigned"
    assert contact.name == create_contact.name
    assert contact.date_of_birth is None

def test_create_existing_contact():
    create_contact = CreateContact(
        name="John Doe",
        date_of_birth=None,
        phone_number="0001112223"
    )
    try:
        _ = commands.add_contact(create_contact)
        _ = commands.add_contact(create_contact)
    except ContactAlreadyExists:
        pass
    else:
        assert False, "Expected ContactAlreadyExists exception was not raised"

def test_update_contact():
    created_contact = commands.add_contact(
        CreateContact(
            name="Jane Doe",
            date_of_birth=None,
            phone_number="0001112227"
        )
    )
    command = UpdateContact(
        name="Jane Smith",
        date_of_birth=date(1990, 10, 27)
    )
    updated_contact = commands.update_contact(created_contact.contact_id, command)

    assert updated_contact.contact_id == created_contact.contact_id, "Contact id hasn't changed"
    assert updated_contact.name == command.name
    assert updated_contact.date_of_birth is not None

def test_delete_contact():
    created_contact = commands.add_contact(
        CreateContact(
            name="Jack Black",
            date_of_birth=None,
            phone_number="0001112225"
        )
    )
    commands.delete_contact(created_contact.contact_id)

def test_delete_contact_by_name():
    created_contact = commands.add_contact(
        CreateContact(
            name="Jack Black",
            date_of_birth=None,
            phone_number="0001112229"
        )
    )
    commands.delete_contact_by_name(created_contact.name)
