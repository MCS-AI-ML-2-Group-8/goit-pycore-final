"""
Domain-specific exceptions for the application.

This module defines custom exceptions used throughout the data layer
to indicate various error conditions such as entities not found or
duplicate entries.
"""


class DomainError(Exception):
    pass

class AlreadyExistsError(Exception):
    pass

class NotFoundError(Exception):
    pass

class ContactNotFound(NotFoundError):
    """
    Raised when contact is not found during command execution
    """

class ContactAlreadyExists(AlreadyExistsError):
    """
    Raised when contact with this name already exists
    """

class PhoneNotFound(NotFoundError):
    """
    Raised when phone is not found during command execution
    """

class PhoneAlreadyExists(AlreadyExistsError):
    """
    Raised when phone with this number already exists
    """

class EmailNotFound(NotFoundError):
    """
    Raised when e-mail is not found during command execution
    """

class EmailAlreadyExists(AlreadyExistsError):
    """
    Raised when e-mail with this address already exists
    """

class NoteNotFound(NotFoundError):
    """
    Raised when text note is not found during command execution
    """

class TagNotFound(NotFoundError):
    """
    Raised when tag is not found during tag removal
    """
