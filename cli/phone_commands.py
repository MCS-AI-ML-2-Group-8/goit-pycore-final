from sqlalchemy import Engine
from pydantic import ValidationError
from cli.database import database_engine
from cli.abstractions import Result
from data.exceptions import ContactNotFound, PhoneAlreadyExists, PhoneNotFound
from data.phone_commands import PhoneCommands, CreatePhone, UpdatePhone
from data.phone_queries import PhoneQueries
from data.models import Phone


class PhoneCommandHandlers:
    commands: PhoneCommands
    queries: PhoneQueries

    def __init__(self, engine: Engine):
        self.commands = PhoneCommands(engine)
        self.queries = PhoneQueries(engine)

    def get_commands(self):
        """
        Returns all commands this handler can process
        """
        return {
            "get-phones": self.get_phones,
            "add-phone": self.add_phone,
            "edit-phone": self.change_phone_number,
            "delete-phone": self.delete_phone
        }

    def get_phones(self, args: list[str]) -> tuple[Result, str]:
        """
        Shows all phones for a contact.
        Returns tuple: status, message
        """
        if len(args) != 1:
            return Result.ERROR, f"ERROR: 'get-phones' command accepts one argument: name. Provided {len(args)} value(s)"

        name = args[0]
        phones = self.queries.get_contact_phones_by_name(name)
        
        if len(phones) == 0:
            return Result.WARNING, f"Contact '{name}' has no phone numbers or contact not found"

        def phone_to_str(phone: Phone):
            return phone.phone_number

        return Result.SUCCESS_DATA, "\n".join(map(phone_to_str, phones))

    def add_phone(self, args: list[str]) -> tuple[Result, str]:
        """
        Adds phone to contact.
        Returns tuple: status, message
        """
        if len(args) != 2:
            return Result.ERROR, f"ERROR: 'add-phone' command accepts two arguments: name and phone number. Provided {len(args)} value(s)"

        name, phone = args
        try:
            _ = self.commands.add_phone_for_contact_by_name(
                contact_name=name,
                command=CreatePhone(phone_number=phone)
            )
            return Result.SUCCESS, "Phone number added."

        except ValidationError:
            return Result.WARNING, f"Phone number '{phone}' has invalid format"

        except ContactNotFound:
            return Result.WARNING, f"Contact '{name}' not found"

        except PhoneAlreadyExists:
            return Result.WARNING, f"Phone number '{phone}' already exists"

    def change_phone_number(self, args: list[str]) -> tuple[Result, str]:
        """
        Changes phone number in address book.
        Returns tuple: status, message
        """
        if len(args) != 3:
            return Result.ERROR, f"ERROR: 'edit-phone' command accepts three arguments: name, old phone number, new phone number. Provided {len(args)} value(s)"

        name, old_phone, new_phone = args
        try:
            _ = self.commands.update_phone_by_number(
                contact_name=name,
                phone_number=old_phone,
                command=UpdatePhone(phone_number=new_phone)
            )
            return Result.SUCCESS, "Phone number changed."

        except ValidationError:
            return Result.WARNING, f"Phone number '{new_phone}' has invalid format"

        except ContactNotFound:
            return Result.WARNING, f"Contact '{name}' not found"

        except PhoneNotFound:
            return Result.WARNING, f"Phone number '{old_phone}' not found"

        except PhoneAlreadyExists:
            return Result.WARNING, f"Phone number '{new_phone}' already exists"

    def delete_phone(self, args: list[str]) -> tuple[Result, str]:
        """
        Deletes phone from contact.
        Returns tuple: status, message
        """
        if len(args) != 2:
            return Result.ERROR, f"ERROR: 'delete-phone' command accepts two arguments: name and phone number. Provided {len(args)} value(s)"

        name, phone = args
        try:
            self.commands.delete_phone_by_number(
                contact_name=name,
                phone_number=phone
            )
            return Result.SUCCESS, "Phone number deleted."

        except ContactNotFound:
            return Result.WARNING, f"Contact '{name}' not found"

        except PhoneNotFound:
            return Result.WARNING, f"Phone number '{phone}' not found"
