from sqlalchemy import Engine
from cli.database import database_engine
from cli.abstractions import Result
from data.phone_commands import PhoneCommands, UpdatePhone
from data.phone_queries import PhoneQueries


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
            "change-phone": self.change_phone_number
        }

    def change_phone_number(self, args: list[str]) -> tuple[Result, str]:
        """
        Changes contact in address book.
        Returns tuple: status, message
        """
        if len(args) != 3:
            return Result.ERROR, f"ERROR: 'change' command accepts three arguments: name, old phone number, new phone number. Provided {len(args)} value(s)"

        name, old_phone, new_phone = args
        commands = PhoneCommands(database_engine)
        _ = commands.update_phone_by_number(
            contact_name=name,
            phone_number=old_phone,
            command=UpdatePhone(phone_number=new_phone)
        )
        return Result.SUCCESS, "Phone number changed."
