"""
Domain commands for tag operations.

This module defines command objects for adding and removing tags
from contacts and notes.
"""

from data.abstractions import DomainCommand

class AddTag(DomainCommand):
    label: str

class RemoveTag(DomainCommand):
    label: str
