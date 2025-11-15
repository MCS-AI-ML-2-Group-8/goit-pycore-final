"""
SQLAlchemy ORM models for the contact management system.

This module defines the database schema including Contact, Phone, Email,
Note, and Tag entities, along with their relationships and association tables.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import override
from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__: str = "contacts"

    contact_id: Mapped[int] = mapped_column("contact_id", Integer, primary_key=True)
    name: Mapped[str] = mapped_column("name", String(64), nullable=False)
    date_of_birth: Mapped[date | None] = mapped_column("date_of_birth", Date, nullable=True)

    phones: Mapped[list[Phone]] = relationship(back_populates="contact", cascade="all", lazy="selectin")
    emails: Mapped[list[Email]] = relationship(back_populates="contact", cascade="all", lazy="selectin")
    notes: Mapped[list[Note]] = relationship(secondary="contact_notes", back_populates="contact", lazy="selectin")
    tags: Mapped[list[Tag]] = relationship(secondary="contact_tags", back_populates="contacts", lazy="selectin")

    @override
    def __repr__(self) -> str:
        return f"Contact({self.name})"


class Phone(Base):
    __tablename__: str = "phones"

    phone_id: Mapped[int] = mapped_column("phone_id", Integer, primary_key=True)
    contact_id: Mapped[int] = mapped_column("contact_id", ForeignKey(Contact.contact_id), nullable=False)
    phone_number: Mapped[str] = mapped_column("phone_number", String(16), nullable=False)

    contact: Mapped[Contact] = relationship(back_populates="phones")

    @override
    def __repr__(self) -> str:
        return f"Phone({self.phone_number})"


class Email(Base):
    __tablename__: str = "emails"

    email_id: Mapped[int] = mapped_column("email_id", Integer, primary_key=True)
    contact_id: Mapped[int] = mapped_column("contact_id", ForeignKey(Contact.contact_id), nullable=False)
    email_address: Mapped[str] = mapped_column("email_address", String(256), nullable=False)

    contact: Mapped[Contact] = relationship(back_populates="emails")

    @override
    def __repr__(self) -> str:
        return f"Email({self.email_address})"


class Note(Base):
    __tablename__: str = "notes"

    note_id: Mapped[int] = mapped_column("note_id", Integer, primary_key=True)
    text: Mapped[str] = mapped_column("text", String, nullable=False)

    contact: Mapped[Contact] = relationship(secondary="contact_notes", back_populates="notes")
    tags: Mapped[list[Tag]] = relationship(secondary="note_tags", back_populates="notes", lazy="selectin")

    @override
    def __repr__(self) -> str:
        return f"Note({self.text[:32]},tags={self.tags})"


class Tag(Base):
    __tablename__: str = "tags"

    tag_id: Mapped[int] = mapped_column("tag_id", Integer, primary_key=True)
    label: Mapped[str] = mapped_column("label", String(64), nullable=False)

    contacts: Mapped[list[Contact]] = relationship(secondary="contact_tags", back_populates="tags")
    notes: Mapped[list[Note]] = relationship(secondary="note_tags", back_populates="tags")

    @override
    def __repr__(self) -> str:
        return f"Tag({self.label})"


class ContactTag(Base):
    __tablename__: str = "contact_tags"

    contact_id: Mapped[int] = mapped_column("contact_id", ForeignKey(Contact.contact_id), primary_key=True)
    tag_id: Mapped[int] = mapped_column("tag_id", ForeignKey(Tag.tag_id), primary_key=True)


class ContactNote(Base):
    __tablename__: str = "contact_notes"

    contact_id: Mapped[int] = mapped_column("contact_id", ForeignKey(Contact.contact_id), primary_key=True)
    note_id: Mapped[int] = mapped_column("note_id", ForeignKey(Note.note_id), primary_key=True)


class NoteTag(Base):
    __tablename__: str = "note_tags"

    note_id: Mapped[int] = mapped_column("note_id", ForeignKey(Note.note_id), primary_key=True)
    tag_id: Mapped[int] = mapped_column("tag_id", ForeignKey(Tag.tag_id), primary_key=True)


@dataclass
class BirthdayReminder:
    contact: Contact
    bidthday: date
