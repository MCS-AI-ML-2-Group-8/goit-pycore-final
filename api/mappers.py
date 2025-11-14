from data.models import Contact, Email, Note, Phone, Tag
from api.models import ContactModel, EmailModel, NoteModel, PhoneModel

def map_contact(contact: Contact) -> ContactModel:
    return ContactModel(
        id=contact.contact_id,
        name=contact.name,
        dateOfBirth=contact.date_of_birth,
        phones=list(map(map_phone, contact.phones)),
        emails=list(map(map_email, contact.emails)),
        notes=list(map(map_note, contact.notes)),
        tags=list(map(map_tag, contact.tags)),
    )

def map_phone(phone: Phone) -> PhoneModel:
    return PhoneModel(id=phone.phone_id, phoneNumber=phone.phone_number)

def map_email(email: Email) -> EmailModel:
    return EmailModel(id=email.email_id, emailAddress=email.email_address)

def map_note(note: Note) -> NoteModel:
    return NoteModel(
        id=note.note_id,
        text=note.text,
        tags=list(map(map_tag, note.tags))
    )

def map_tag(tag: Tag) -> str:
    return tag.label
