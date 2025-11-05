from sqlalchemy import Engine
from cli.abstractions import Result
from data.contact_commands import ContactCommands, CreateContact
from data.contact_queries import ContactQueries
from data.models import Contact


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
            "all": self.get_all,
            "add": self.add_contact
        }

    def add_contact(self, args: list[str]) -> tuple[Result, str]:
        """
        Adds contact to address book.
        Returns tuple: status, message
        """
        if len(args) != 2:
            return Result.ERROR, f"ERROR: 'add' command accepts two arguments: name and phone number. Provided {len(args)} value(s)"

        name, phone = args
        _ = self.commands.add_contact(
            CreateContact(
                name=name,
                phone_number=phone,
                date_of_birth=None
            )
        )
        return Result.SUCCESS, "Contact created."


    def get_all(self, _: list[str]) -> tuple[Result, str]:
        """
        Returns all contacts from address book.
        Returns tuple: status, contacts text representation
        """
        contacts = self.queries.get_contacts()
        if len(contacts) == 0:
            return Result.WARNING, "Contact book is empty"

        def contact_to_str(contact: Contact):
            phones = ", ".join([phone.phone_number for phone in contact.phones])
            birthday_after_pipe = f" | Birthday: {contact.date_of_birth.strftime("%d.%m.%Y")}" if  contact.date_of_birth else ""
            return f"{contact.name} ({phones}){birthday_after_pipe}"

        return Result.SUCCESS_DATA, "\n".join(map(contact_to_str, contacts))
