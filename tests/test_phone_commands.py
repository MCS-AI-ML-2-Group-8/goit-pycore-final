from sqlalchemy import create_engine
from data.models import Base
from data.exceptions import ContactNotFound, PhoneAlreadyExists, PhoneNotFound
from data.contact_commands import ContactCommands, CreateContact
from data.phone_commands import PhoneCommands, CreatePhone, UpdatePhone

engine = create_engine("sqlite:///:memory:")
contact_commands = ContactCommands(engine)
commands = PhoneCommands(engine)

Base.metadata.create_all(engine)

def test_add_phone_for_contact():
    contact = contact_commands.add_contact(
        CreateContact(
            name="John Doe",
            date_of_birth=None,
            phone_number="1111111111"
        )
    )
    command = CreatePhone(phone_number="2222222222")
    phone = commands.add_phone_for_contact(contact.contact_id, command)

    assert phone.phone_id != 0, "Phone does not have id assigned"
    assert phone.phone_number == command.phone_number
    assert phone.contact_id == contact.contact_id

def test_add_phone_for_non_existent_contact():
    try:
        _ = commands.add_phone_for_contact(
            999999,
            CreatePhone(phone_number="3333333333")
        )
    except ContactNotFound:
        pass
    else:
        assert False, "Expected ContactNotFound exception was not raised"

def test_add_duplicate_phone():
    contact = contact_commands.add_contact(
        CreateContact(
            name="Jane Doe",
            date_of_birth=None,
            phone_number="4444444444"
        )
    )
    try:
        _ = commands.add_phone_for_contact(
            contact.contact_id,
            CreatePhone(phone_number="4444444444")
        )
    except PhoneAlreadyExists:
        pass
    else:
        assert False, "Expected PhoneAlreadyExists exception was not raised"

def test_update_phone():
    contact = contact_commands.add_contact(
        CreateContact(
            name="Bob Smith",
            date_of_birth=None,
            phone_number="5555555555"
        )
    )
    phone_id = contact.phones[0].phone_id
    command = UpdatePhone(phone_number="6666666666")
    updated_phone = commands.update_phone(phone_id, command)
    assert updated_phone.phone_id == phone_id, "Phone id hasn't changed"
    assert updated_phone.phone_number == command.phone_number

def test_update_non_existent_phone():
    try:
        _ = commands.update_phone(
            999999,
            UpdatePhone(phone_number="7777777777")
        )
    except PhoneNotFound:
        pass
    else:
        assert False, "Expected PhoneNotFound exception was not raised"

def test_update_phone_with_duplicate_number():
    contact = contact_commands.add_contact(
        CreateContact(
            name="Alice Johnson",
            date_of_birth=None,
            phone_number="8888888888"
        )
    )
    second_phone = commands.add_phone_for_contact(
        contact.contact_id,
        CreatePhone(phone_number="9999999999")
    )
    try:
        _ = commands.update_phone(
            second_phone.phone_id,
            UpdatePhone(phone_number="8888888888")
        )
    except PhoneAlreadyExists:
        pass
    else:
        assert False, "Expected PhoneAlreadyExists exception was not raised"

def test_update_phone_by_number():
    contact = contact_commands.add_contact(
        CreateContact(
            name="Charlie Brown",
            date_of_birth=None,
            phone_number="1010101010"
        )
    )
    command = UpdatePhone(phone_number="2020202020")
    updated_phone = commands.update_phone_by_number(
        contact.name,
        "1010101010",
        command
    )

    assert updated_phone.phone_number == command.phone_number
    assert updated_phone.contact_id == contact.contact_id

def test_update_phone_by_number_non_existent():
    try:
        _ = commands.update_phone_by_number(
            "Nonexistent Contact",
            "4040404040",
            UpdatePhone(phone_number="3030303030")
        )
    except PhoneNotFound:
        pass
    else:
        assert False, "Expected PhoneNotFound exception was not raised"

def test_update_phone_by_number_with_duplicate():
    contact = contact_commands.add_contact(
        CreateContact(
            name="David Lee",
            date_of_birth=None,
            phone_number="5050505050"
        )
    )
    _ = commands.add_phone_for_contact(
        contact.contact_id,
        CreatePhone(phone_number="6060606060")
    )
    # Try to update the second phone to the first phone's number
    try:
        _ = commands.update_phone_by_number(
            contact.name,
            "6060606060",
            UpdatePhone(phone_number="5050505050")
        )
    except PhoneAlreadyExists:
        pass
    else:
        assert False, "Expected PhoneAlreadyExists exception was not raised"

def test_delete_phone():
    contact = contact_commands.add_contact(
        CreateContact(
            name="Eve Wilson",
            date_of_birth=None,
            phone_number="7070707070"
        )
    )
    phone_id = contact.phones[0].phone_id
    commands.delete_phone(phone_id)

def test_delete_non_existent_phone():
    try:
        commands.delete_phone(999999)
    except PhoneNotFound:
        pass
    else:
        assert False, "Expected PhoneNotFound exception was not raised"

def test_delete_phone_by_number():
    contact = contact_commands.add_contact(
        CreateContact(
            name="Frank Miller",
            date_of_birth=None,
            phone_number="8080808080"
        )
    )
    commands.delete_phone_by_number(contact.name, "8080808080")

def test_delete_phone_by_number_non_existent():
    try:
        commands.delete_phone_by_number(
            "Nonexistent Contact",
            "9090909090"
        )
    except PhoneNotFound:
        pass
    else:
        assert False, "Expected PhoneNotFound exception was not raised"
