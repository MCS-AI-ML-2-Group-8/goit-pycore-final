"""
CLI command handlers for note operations.

This module provides CLI command handlers for managing notes,
both standalone and contact-associated, including tag management
and text search functionality.
"""

from sqlalchemy import Engine
from cli.abstractions import Result
from data.exceptions import ContactNotFound, NoteNotFound, TagNotFound
from data.note_commands import NoteCommands, CreateNote, UpdateNote
from data.note_queries import NoteQueries
from data.models import Note
from data.tag_commands import AddTag, RemoveTag


class NoteCommandHandlers:
    commands: NoteCommands
    queries: NoteQueries

    def __init__(self, engine: Engine):
        self.commands = NoteCommands(engine)
        self.queries = NoteQueries(engine)

    @staticmethod
    def list_note_texts(engine: Engine) -> list[str]:
        queries = NoteQueries(engine)
        notes = [note.text for note in queries.get_notes()]
        return notes

    @staticmethod
    def list_note_tags(engine: Engine) -> list[str]:
        queries = NoteQueries(engine)
        tags: set[str] = set()
        tags = { tag.label for note in queries.get_notes() for tag in note.tags }
        return list(sorted(tags))

    def get_commands(self):
        """
        Returns all commands this handler can process
        """
        return {
            "get-notes": self.get_notes,
            "add-note": self.add_note,
            "edit-note": self.edit_note,
            "delete-note": self.delete_note,
            "add-tag-to-note": self.add_tag_to_note,
            "remove-tag-from-note": self.remove_tag_from_note,
            "get-contact-notes": self.get_contact_notes,
            "add-note-to-contact": self.add_note_to_contact
        }

    def get_notes(self, args: list[str]) -> tuple[Result, str]:
        """
        Shows all notes or notes filtered by tag.
        Returns tuple: status, message
        """
        if len(args) == 0:
            notes = self.queries.get_notes()
        elif len(args) == 1:
            tag = args[0]
            notes = self.queries.get_notes_by_tag(tag)
        else:
            return Result.ERROR, f"ERROR: 'get-notes' command accepts zero or one argument: [tag]. Provided {len(args)} value(s)"

        if len(notes) == 0:
            return Result.WARNING, "No notes found"

        def note_to_str(note: Note):
            tags = ", ".join([tag.label for tag in note.tags]) if note.tags else "No tags"
            return f"{note.text} | Tags: {tags}"

        return Result.SUCCESS_DATA, "\n".join(map(note_to_str, notes))

    def get_contact_notes(self, args: list[str]) -> tuple[Result, str]:
        """
        Shows all notes for a contact, optionally filtered by tag.
        Returns tuple: status, message
        """
        if len(args) == 1:
            name = args[0]
            notes = self.queries.get_notes_for_contact_by_name(name)
        elif len(args) == 2:
            name, tag = args
            notes = self.queries.get_notes_for_contact_by_name_and_tag(name, tag)
        else:
            return Result.ERROR, f"ERROR: 'get-contact-notes' command accepts one or two arguments: name [tag]. Provided {len(args)} value(s)"

        if len(notes) == 0:
            return Result.WARNING, f"No notes found for contact '{args[0]}'"

        def note_to_str(note: Note):
            tags = ", ".join([tag.label for tag in note.tags]) if note.tags else "No tags"
            return f"{note.text} | Tags: {tags}"

        return Result.SUCCESS_DATA, "\n".join(map(note_to_str, notes))

    def add_note(self, args: list[str]) -> tuple[Result, str]:
        """
        Adds a standalone note with tag.
        Returns tuple: status, message
        """
        if len(args) != 2:
            return Result.ERROR, f"ERROR: 'add-note' command accepts two arguments: text and tag. Provided {len(args)} value(s)"

        text, tag = args
        try:
            note = self.commands.add_note(CreateNote(text=text))
            self.commands.add_tag_to_note(note.note_id, AddTag(label=tag))
            return Result.SUCCESS, "Note created."

        except Exception as e:
            return Result.WARNING, f"Failed to create note: {e}"

    def add_note_to_contact(self, args: list[str]) -> tuple[Result, str]:
        """
        Adds a note to a contact with tag.
        Returns tuple: status, message
        """
        if len(args) != 3:
            return Result.ERROR, f"ERROR: 'add-note-to-contact' command accepts three arguments: name, text, and tag. Provided {len(args)} value(s)"

        name, text, tag = args
        try:
            note = self.commands.add_note_for_contact_by_name(name, CreateNote(text=text))
            self.commands.add_tag_to_note(note.note_id, AddTag(label=tag))
            return Result.SUCCESS, "Note added to contact."

        except ContactNotFound:
            return Result.WARNING, f"Contact '{name}' not found"

    def edit_note(self, args: list[str]) -> tuple[Result, str]:
        """
        Edits a note found by text fragment.
        Returns tuple: status, message
        """
        if len(args) != 2:
            return Result.ERROR, f"ERROR: 'edit-note' command accepts two arguments: text fragment and new text. Provided {len(args)} value(s)"

        fragment, new_text = args
        try:
            _ = self.commands.update_note_by_fragment(fragment, UpdateNote(text=new_text))
            return Result.SUCCESS, "Note updated."

        except NoteNotFound:
            return Result.WARNING, f"Note containing '{fragment}' not found"

    def delete_note(self, args: list[str]) -> tuple[Result, str]:
        """
        Deletes a note found by text fragment.
        Returns tuple: status, message
        """
        if len(args) != 1:
            return Result.ERROR, f"ERROR: 'delete-note' command accepts one argument: text fragment. Provided {len(args)} value(s)"

        fragment = args[0]
        try:
            self.commands.delete_note_from_fragment(fragment)
            return Result.SUCCESS, "Note deleted."

        except NoteNotFound:
            return Result.WARNING, f"Note containing '{fragment}' not found"

    def add_tag_to_note(self, args: list[str]) -> tuple[Result, str]:
        """
        Adds tag to a note found by text fragment.
        Returns tuple: status, message
        """
        if len(args) != 2:
            return Result.ERROR, f"ERROR: 'add-tag-to-note' command accepts two arguments: text fragment and tag. Provided {len(args)} value(s)"

        fragment, tag = args
        try:
            self.commands.add_tag_to_note_by_fragment(fragment, AddTag(label=tag))
            return Result.SUCCESS, "Tag added to note."

        except NoteNotFound:
            return Result.WARNING, f"Note containing '{fragment}' not found"

    def remove_tag_from_note(self, args: list[str]) -> tuple[Result, str]:
        """
        Removes tag from a note found by text fragment.
        Returns tuple: status, message
        """
        if len(args) != 2:
            return Result.ERROR, f"ERROR: 'remove-tag-from-note' command accepts two arguments: text fragment and tag. Provided {len(args)} value(s)"

        fragment, tag = args
        try:
            self.commands.remove_tag_from_note_by_fragment(fragment, RemoveTag(label=tag))
            return Result.SUCCESS, "Tag removed from note."

        except NoteNotFound:
            return Result.WARNING, f"Note containing '{fragment}' not found"

        except TagNotFound:
            return Result.WARNING, f"Tag '{tag}' not found"
