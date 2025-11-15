import { useState } from "react";
import "./ContactCard.css";

interface Email {
  id: number;
  emailAddress: string;
}

interface Phone {
  id: number;
  phoneNumber: string;
}

interface Note {
  id: number;
  text: string;
  tags: string[];
}

interface Contact {
  id: number;
  name: string;
  dateOfBirth: string;
  emails: Email[];
  phones: Phone[];
  tags: string[];
  notes: Note[];
}

const ContactCard = ({ contact }: { contact: Contact }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleAccordion = () => {
    setIsOpen(!isOpen);
  };

  if (!contact) {
    return null;
  }

  return (
    <div className="contact-card">
      <div className="card-header" onClick={toggleAccordion}>
        <h3 className="contact-name">{contact.name}</h3>
        <div className="header-right">
          {contact.dateOfBirth && (
            <span className="contact-birthday">
              🎂 {new Date(contact.dateOfBirth).toLocaleDateString()}
            </span>
          )}
          <span className={`accordion-icon ${isOpen ? "open" : ""}`}> ↕️ </span>
        </div>
      </div>
      <div className={`card-body ${isOpen ? "open" : ""}`}>
        {contact.emails && contact.emails.length > 0 && (
          <div className="contact-section">
            <h4>Emails:</h4>
            <ul>
              {contact.emails.map((email) => (
                <li key={email.id}>{email.emailAddress}</li>
              ))}
            </ul>
          </div>
        )}
        {contact.phones && contact.phones.length > 0 && (
          <div className="contact-section">
            <h4>Phones:</h4>
            <ul>
              {contact.phones.map((phone) => (
                <li key={phone.id}>{phone.phoneNumber}</li>
              ))}
            </ul>
          </div>
        )}
        {contact.tags && contact.tags.length > 0 && (
          <div className="contact-section">
            <h4>Tags:</h4>
            <div className="contact-tags">
              {contact.tags.map((tag, i) => (
                <span key={i} className="tag">
                  {tag}
                </span>
              ))}
            </div>
          </div>
        )}
        {contact.notes && contact.notes.length > 0 && (
          <div className="contact-section">
            <h4>Notes:</h4>
            <ul className="notes-list">
              {contact.notes.map((note) => (
                <li key={note.id} className="note-item">
                  <p>{note.text}</p>
                  {note.tags && note.tags.length > 0 && (
                    <div className="note-tags">
                      {note.tags.map((tag, i) => (
                        <span key={i} className="tag note-tag">
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default ContactCard;
