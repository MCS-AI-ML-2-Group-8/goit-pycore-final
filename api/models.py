from datetime import date
from pydantic import BaseModel

class PhoneModel(BaseModel):
    id: int
    phoneNumber: str

class EmailModel(BaseModel):
    id: int
    emailAddress: str

class NoteModel(BaseModel):
    id: int
    text: str

class ContactModel(BaseModel):
    id: int
    name: str
    dateOfBirth: date | None
    phones: list[PhoneModel]
    emails: list[EmailModel]
    notes: list[NoteModel]
    tags: list[str]
