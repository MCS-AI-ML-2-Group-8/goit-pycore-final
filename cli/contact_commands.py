"""
CLI command handlers for contact operations.

This module provides CLI command handlers for managing contacts,
including CRUD operations and tag management.
"""

from pydantic import ValidationError
from sqlalchemy import Engine
from cli.abstractions import Result
from data.contact_commands import ContactCommands, CreateContact, UpdateContact
from data.contact_queries import ContactQueries
from data.exceptions import ContactAlreadyExists, ContactNotFound, PhoneAlreadyExists, TagNotFound
from data.models import Contact
from data.tag_commands import AddTag, RemoveTag


class ContactCommandHandlers:
    commands: ContactCommands
    queries: ContactQueries

    def __init__(self, engine: Engine):
        self.commands = ContactCommands(engine)
        self.queries = ContactQueries(engine)

    def get_commands(self):
        """
        Returns all commands this handler can process
        """
        return {
            "get-contacts": self.get_contacts,
            "get-contact": self.get_contact,
            "add-contact": self.add_contact,
            "edit-contact": self.edit_contact,
            "delete-contact": self.delete_contact,
            "add-tag-to-contact": self.add_tag_to_contact,
            "remove-tag-from-contact": self.remove_tag_from_contact
        }

    
    def get_contacts(self, args: list[str]) -> tuple[Result, str]:
        """
        Returns all contacts or contacts filtered by tag.
        Returns tuple: status, contacts text representation
        """
        if len(args) == 0:
            contacts = self.queries.get_contacts()
        elif len(args) == 1:
            tag = args[0]
            contacts = self.queries.get_contacts_by_tag(tag)
        else:
            return Result.ERROR, f"ERROR: 'get-contacts' command accepts zero or one argument: [tag]. Provided {len(args)} value(s)"

        if len(contacts) == 0:
            return Result.WARNING, "No contacts found"

        def contact_to_str(contact: Contact):
            phones = ", ".join([phone.phone_number for phone in contact.phones])
            birthday_after_pipe = f" | Birthday: {contact.date_of_birth.strftime("%d.%m.%Y")}" if contact.date_of_birth else ""
            tags = ", ".join([tag.label for tag in contact.tags]) if contact.tags else ""
            tags_after_pipe = f" | Tags: {tags}" if tags else ""
            return f"{contact.name} ({phones}){birthday_after_pipe}{tags_after_pipe}"

        return Result.SUCCESS_DATA, "\n".join(map(contact_to_str, contacts))

    def get_contact(self, args: list[str]) -> tuple[Result, str]:
        """
        Shows detailed information about a contact.
        Returns tuple: status, contact details
        """
        if len(args) != 1:
            return Result.ERROR, f"ERROR: 'get-contact' command accepts one argument: name. Provided {len(args)} value(s)"

        name = args[0]
        contact = self.queries.get_contact_by_name(name)
        
        if not contact:
            return Result.WARNING, f"Contact '{name}' not found"

        phones = ", ".join([phone.phone_number for phone in contact.phones]) if contact.phones else "No phones"
        emails = ", ".join([email.email_address for email in contact.emails]) if contact.emails else "No emails"
        birthday = contact.date_of_birth.strftime("%d.%m.%Y") if contact.date_of_birth else "Not set"
        tags = ", ".join([tag.label for tag in contact.tags]) if contact.tags else "No tags"
        
        details = f"""Name: {contact.name}
Phones: {phones}
Emails: {emails}
Birthday: {birthday}
Tags: {tags}"""
        
        return Result.SUCCESS_DATA, details

    def add_contact(self, args: list[str]) -> tuple[Result, str]:
        """
        Adds contact to address book.
        Returns tuple: status, message
        """
        if len(args) != 2:
            return Result.ERROR, f"ERROR: 'add-contact' command accepts two arguments: name and phone number. Provided {len(args)} value(s)"

        name, phone = args
        try:
            _ = self.commands.add_contact(
                CreateContact(
                    name=name,
                    phone_number=phone,
                    date_of_birth=None
                )
            )
            return Result.SUCCESS, "Contact created."

        except ValidationError:
            return Result.WARNING, f"Phone number '{phone}' has invalid format"

        except ContactAlreadyExists:
            return Result.WARNING, f"Contact '{name}' already exists"

        except PhoneAlreadyExists:
            return Result.WARNING, f"Phone number '{phone}' already exists"

    def edit_contact(self, args: list[str]) -> tuple[Result, str]:
        """
        Changes contact name.
        Returns tuple: status, message
        """
        if len(args) != 2:
            return Result.ERROR, f"ERROR: 'edit-contact' command accepts two arguments: name and new name. Provided {len(args)} value(s)"

        name, new_name = args
        try:
            contact = self.queries.get_contact_by_name(name)
            if not contact:
                raise ContactNotFound()

            _ = self.commands.update_contact_by_name(
                contact_name=name,
                command=UpdateContact(
                    name=new_name,
                    date_of_birth=contact.date_of_birth
                )
            )
            return Result.SUCCESS, "Contact name changed."

        except ContactNotFound:
            return Result.WARNING, f"Contact '{name}' not found"

        except ContactAlreadyExists:
            return Result.WARNING, f"Contact '{new_name}' already exists"

    def delete_contact(self, args: list[str]) -> tuple[Result, str]:
        """
        Deletes a contact.
        Returns tuple: status, message
        """
        if len(args) != 1:
            return Result.ERROR, f"ERROR: 'delete-contact' command accepts one argument: name. Provided {len(args)} value(s)"

        name = args[0]
        try:
            self.commands.delete_contact_by_name(name)
            return Result.SUCCESS, "Contact deleted."

        except ContactNotFound:
            return Result.WARNING, f"Contact '{name}' not found"

    def add_tag_to_contact(self, args: list[str]) -> tuple[Result, str]:
        """
        Adds tag to contact.
        Returns tuple: status, message
        """
        if len(args) != 2:
            return Result.ERROR, f"ERROR: 'add-tag-to-contact' command accepts two arguments: name and tag. Provided {len(args)} value(s)"

        name, tag = args
        try:
            self.commands.add_tag_to_contact_by_name(
                contact_name=name,
                command=AddTag(label=tag)
            )
            return Result.SUCCESS, "Tag added to contact."

        except ContactNotFound:
            return Result.WARNING, f"Contact '{name}' not found"

    def remove_tag_from_contact(self, args: list[str]) -> tuple[Result, str]:
        """
        Removes tag from contact.
        Returns tuple: status, message
        """
        if len(args) != 2:
            return Result.ERROR, f"ERROR: 'remove-tag-from-contact' command accepts two arguments: name and tag. Provided {len(args)} value(s)"

        name, tag = args
        try:
            self.commands.remove_tag_from_contact_by_name(
                contact_name=name,
                command=RemoveTag(label=tag)
            )
            return Result.SUCCESS, "Tag removed from contact."

        except ContactNotFound:
            return Result.WARNING, f"Contact '{name}' not found"

        except TagNotFound:
            return Result.WARNING, f"Tag '{tag}' not found"
