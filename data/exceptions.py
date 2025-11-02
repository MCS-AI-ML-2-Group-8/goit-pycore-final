class DomainException(Exception):
    pass

class ContactNotFound(DomainException):
    """
    Raised when contact is not found during command execution
    """

class ContactAlreadyExists(DomainException):
    """
    Raised when contact with this name already exists
    """

class PhoneNotFound(DomainException):
    """
    Raised when phone is not found during command execution
    """

class PhoneAlreadyExists(DomainException):
    """
    Raised when phone with this number already exists
    """
