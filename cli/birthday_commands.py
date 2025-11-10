from datetime import datetime
from sqlalchemy import Engine
from cli.abstractions import Result
from data.exceptions import ContactNotFound
from data.contact_commands import ContactCommands, UpdateContact
from data.contact_queries import ContactQueries
from data.models import Contact


class BirthdayCommandHandlers:
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
            "add-birthday": self.add_birthday,
            "remove-birthday": self.remove_birthday,
            "get-birthdays": self.get_birthdays
        }

    def add_birthday(self, args: list[str]) -> tuple[Result, str]:
        """
        Adds or updates birthday for a contact.
        Returns tuple: status, message
        """
        if len(args) != 2:
            return Result.ERROR, f"ERROR: 'add-birthday' command accepts two arguments: name and date (YYYY-MM-DD). Provided {len(args)} value(s)"

        name, date_str = args
        
        try:
            # Parse the date
            birthday = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Result.WARNING, f"Invalid date format '{date_str}'. Use YYYY-MM-DD format (e.g., 1985-03-20)"

        try:
            _ = self.commands.update_contact_by_name(
                contact_name=name,
                command=UpdateContact(
                    name=name,
                    date_of_birth=birthday
                )
            )
            return Result.SUCCESS, "Birthday added."

        except ContactNotFound:
            return Result.WARNING, f"Contact '{name}' not found"

    def remove_birthday(self, args: list[str]) -> tuple[Result, str]:
        """
        Removes birthday from a contact.
        Returns tuple: status, message
        """
        if len(args) != 1:
            return Result.ERROR, f"ERROR: 'remove-birthday' command accepts one argument: name. Provided {len(args)} value(s)"

        name = args[0]
        
        try:
            _ = self.commands.update_contact_by_name(
                contact_name=name,
                command=UpdateContact(
                    name=name,
                    date_of_birth=None
                )
            )
            return Result.SUCCESS, "Birthday removed."

        except ContactNotFound:
            return Result.WARNING, f"Contact '{name}' not found"

    def get_birthdays(self, args: list[str]) -> tuple[Result, str]:
        """
        Shows contacts with birthdays in the next N days.
        Returns tuple: status, message
        """
        if len(args) != 1:
            return Result.ERROR, f"ERROR: 'get-birthdays' command accepts one argument: number of days. Provided {len(args)} value(s)"

        try:
            days = int(args[0])
            if days < 0:
                return Result.WARNING, "Number of days must be positive"
        except ValueError:
            return Result.WARNING, f"Invalid number '{args[0]}'. Please provide a valid integer"

        try:
            contacts = self.queries.get_contacts_with_birthdays_in_days(days)
            
            if len(contacts) == 0:
                return Result.WARNING, f"No birthdays in the next {days} day(s)"

            def contact_to_str(contact: Contact):
                birthday_str = contact.date_of_birth.strftime("%d.%m.%Y") if contact.date_of_birth else "Unknown"
                return f"{contact.name} - {birthday_str}"

            return Result.SUCCESS_DATA, "\n".join(map(contact_to_str, contacts))

        except NotImplementedError as e:
            return Result.WARNING, str(e)
