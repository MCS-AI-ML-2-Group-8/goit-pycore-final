"""
CLI command handlers for email address operations.

This module provides CLI command handlers for managing email addresses
associated with contacts, including add, edit, and delete operations.
"""

from sqlalchemy import Engine
from pydantic import ValidationError
from cli.abstractions import Result
from data.exceptions import ContactNotFound, EmailAlreadyExists, EmailNotFound
from data.email_commands import EmailCommands, CreateEmail, UpdateEmail
from data.email_queries import EmailQueries
from data.models import Email


class EmailCommandHandlers:
    commands: EmailCommands
    queries: EmailQueries

    def __init__(self, engine: Engine):
        self.commands = EmailCommands(engine)
        self.queries = EmailQueries(engine)

    def get_commands(self):
        """
        Returns all commands this handler can process
        """
        return {
            "get-emails": self.get_emails,
            "add-email": self.add_email,
            "edit-email": self.change_email,
            "delete-email": self.delete_email
        }

    def get_emails(self, args: list[str]) -> tuple[Result, str]:
        """
        Shows all emails for a contact.
        Returns tuple: status, message
        """
        if len(args) != 1:
            return Result.ERROR, f"ERROR: 'get-emails' command accepts one argument: name. Provided {len(args)} value(s)"

        name = args[0]
        emails = self.queries.get_contact_emails_by_name(name)
        
        if len(emails) == 0:
            return Result.WARNING, f"Contact '{name}' has no email addresses or contact not found"

        def email_to_str(email: Email):
            return email.email_address

        return Result.SUCCESS_DATA, "\n".join(map(email_to_str, emails))

    def add_email(self, args: list[str]) -> tuple[Result, str]:
        """
        Adds email to contact.
        Returns tuple: status, message
        """
        if len(args) != 2:
            return Result.ERROR, f"ERROR: 'add-email' command accepts two arguments: name and email address. Provided {len(args)} value(s)"

        name, email = args
        try:
            _ = self.commands.add_email_for_contact_by_name(
                contact_name=name,
                command=CreateEmail(email_address=email)
            )
            return Result.SUCCESS, "Email address added."

        except ValidationError:
            return Result.WARNING, f"Email address '{email}' has invalid format"

        except ContactNotFound:
            return Result.WARNING, f"Contact '{name}' not found"

        except EmailAlreadyExists:
            return Result.WARNING, f"Email address '{email}' already exists"

    def change_email(self, args: list[str]) -> tuple[Result, str]:
        """
        Changes email address in address book.
        Returns tuple: status, message
        """
        if len(args) != 3:
            return Result.ERROR, f"ERROR: 'edit-email' command accepts three arguments: name, old email, new email. Provided {len(args)} value(s)"

        name, old_email, new_email = args
        try:
            _ = self.commands.update_email_by_address(
                contact_name=name,
                email_address=old_email,
                command=UpdateEmail(email_address=new_email)
            )
            return Result.SUCCESS, "Email address changed."

        except ValidationError:
            return Result.WARNING, f"Email address '{new_email}' has invalid format"

        except ContactNotFound:
            return Result.WARNING, f"Contact '{name}' not found"

        except EmailNotFound:
            return Result.WARNING, f"Email address '{old_email}' not found"

        except EmailAlreadyExists:
            return Result.WARNING, f"Email address '{new_email}' already exists"

    def delete_email(self, args: list[str]) -> tuple[Result, str]:
        """
        Deletes email from contact.
        Returns tuple: status, message
        """
        if len(args) != 2:
            return Result.ERROR, f"ERROR: 'delete-email' command accepts two arguments: name and email address. Provided {len(args)} value(s)"

        name, email = args
        try:
            self.commands.delete_email_by_address(
                contact_name=name,
                email_address=email
            )
            return Result.SUCCESS, "Email address deleted."

        except ContactNotFound:
            return Result.WARNING, f"Contact '{name}' not found"

        except EmailNotFound:
            return Result.WARNING, f"Email address '{email}' not found"
