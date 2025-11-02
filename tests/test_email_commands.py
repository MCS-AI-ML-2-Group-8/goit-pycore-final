from sqlalchemy import create_engine
from data.models import Base
from data.exceptions import ContactNotFound, EmailAlreadyExists, EmailNotFound
from data.contact_commands import ContactCommands, CreateContact
from data.email_commands import EmailCommands, CreateEmail, UpdateEmail

engine = create_engine("sqlite:///:memory:")
contact_commands = ContactCommands(engine)
commands = EmailCommands(engine)

Base.metadata.create_all(engine)

def test_add_email_for_contact():
    contact = contact_commands.add_contact(
        CreateContact(
            name="John Doe",
            date_of_birth=None,
            phone_number="1111111111"
        )
    )
    command = CreateEmail(email_address="john@example.com")
    email = commands.add_email_for_contact(contact.contact_id, command)

    assert email.email_id != 0, "Email does not have id assigned"
    assert email.email_address == command.email_address
    assert email.contact_id == contact.contact_id

def test_add_email_for_non_existent_contact():
    try:
        _ = commands.add_email_for_contact(
            999999,
            CreateEmail(email_address="nonexistent@example.com")
        )
    except ContactNotFound:
        pass
    else:
        assert False, "Expected ContactNotFound exception was not raised"

def test_add_duplicate_email():
    contact = contact_commands.add_contact(
        CreateContact(
            name="Jane Doe",
            date_of_birth=None,
            phone_number="2222222222"
        )
    )
    _ = commands.add_email_for_contact(
        contact.contact_id,
        CreateEmail(email_address="jane@example.com")
    )
    try:
        _ = commands.add_email_for_contact(
            contact.contact_id,
            CreateEmail(email_address="jane@example.com")
        )
    except EmailAlreadyExists:
        pass
    else:
        assert False, "Expected EmailAlreadyExists exception was not raised"

def test_update_email():
    contact = contact_commands.add_contact(
        CreateContact(
            name="Bob Smith",
            date_of_birth=None,
            phone_number="3333333333"
        )
    )
    email = commands.add_email_for_contact(
        contact.contact_id,
        CreateEmail(email_address="bob@example.com")
    )
    command = UpdateEmail(email_address="bob.smith@example.com")
    updated_email = commands.update_email(email.email_id, command)

    assert updated_email.email_id == email.email_id, "Email id hasn't changed"
    assert updated_email.email_address == command.email_address

def test_update_non_existent_email():
    try:
        _ = commands.update_email(
            999999,
            UpdateEmail(email_address="nonexistent@example.com")
        )
    except EmailNotFound:
        pass
    else:
        assert False, "Expected EmailNotFound exception was not raised"

def test_update_email_with_duplicate_address():
    contact = contact_commands.add_contact(
        CreateContact(
            name="Alice Johnson",
            date_of_birth=None,
            phone_number="4444444444"
        )
    )
    _ = commands.add_email_for_contact(
        contact.contact_id,
        CreateEmail(email_address="alice@example.com")
    )
    second_email = commands.add_email_for_contact(
        contact.contact_id,
        CreateEmail(email_address="alice.j@example.com")
    )
    try:
        _ = commands.update_email(
            second_email.email_id,
            UpdateEmail(email_address="alice@example.com")
        )
    except EmailAlreadyExists:
        pass
    else:
        assert False, "Expected EmailAlreadyExists exception was not raised"

def test_update_email_by_address():
    contact = contact_commands.add_contact(
        CreateContact(
            name="Charlie Brown",
            date_of_birth=None,
            phone_number="5555555555"
        )
    )
    _ = commands.add_email_for_contact(
        contact.contact_id,
        CreateEmail(email_address="charlie@example.com")
    )
    command = UpdateEmail(email_address="charlie.brown@example.com")
    updated_email = commands.update_email_by_address(
        contact.name,
        "charlie@example.com",
        command
    )

    assert updated_email.email_address == command.email_address
    assert updated_email.contact_id == contact.contact_id

def test_delete_email():
    contact = contact_commands.add_contact(
        CreateContact(
            name="Eve Wilson",
            date_of_birth=None,
            phone_number="6666666666"
        )
    )
    email = commands.add_email_for_contact(
        contact.contact_id,
        CreateEmail(email_address="eve@example.com")
    )
    commands.delete_email(email.email_id)

def test_delete_non_existent_email():
    try:
        commands.delete_email(999999)
    except EmailNotFound:
        pass
    else:
        assert False, "Expected EmailNotFound exception was not raised"

def test_delete_email_by_address():
    contact = contact_commands.add_contact(
        CreateContact(
            name="Frank Miller",
            date_of_birth=None,
            phone_number="7777777777"
        )
    )
    _ = commands.add_email_for_contact(
        contact.contact_id,
        CreateEmail(email_address="frank@example.com")
    )
    commands.delete_email_by_address(contact.name, "frank@example.com")
