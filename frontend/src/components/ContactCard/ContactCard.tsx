import { useState, useEffect } from "react";
import "./ContactCard.css";
import { FaBirthdayCake } from "react-icons/fa";
import { LuArrowDownWideNarrow } from "react-icons/lu";
import EditButton from "../Buttons/EditButton";
import { updateContact } from "../../api/api";
import EditableInput from "../Inputs/EditInput";
import PhoneSection from "./PhoneSection";
import EmailSection from "./EmailSection";
import NoteSection from "./NoteSection";
import TagSection from "./TagSection";


const ContactCard = ({ contact }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [newName, setNewName] = useState(contact.name);
  const [localContact, setLocalContact] = useState(contact);

  useEffect(() => {
    setLocalContact(contact);
    setNewName(contact.name);
  }, [contact]);

  // open cart
  const toggleAccordion = () => {
    setIsOpen(!isOpen);
  };

  //  edit control
  const handleEdit = () => {
    setIsEditing(true);
  };

  //  contact change
  const handleSave = async () => {
    try {
      await updateContact(contact.id, {
        name: newName,
        date_of_birth: contact.dateOfBirth || null,
      });
      setLocalContact({ ...localContact, name: newName });
      setIsEditing(false);
    } catch (error) {
      console.error("Error updating contact:", error);
    }
  };

  const handleCancel = () => {
    setNewName(contact.name);
    setIsEditing(false);
  };

  if (!localContact) {
    return null;
  }

  return (
    <div className="contact-card">
      <div className="card-header">
        <div className="flex justify-between items-center">
          {isEditing ? (
            <EditableInput
              value={newName}
              onChange={setNewName}
              onSave={handleSave}
              onCancel={handleCancel}
              className={"opacity-100"}
            />
          ) : (
            <h3 className="text-lg font-bold flex items-center gap-0.5 text-indigo-100">
              {localContact.name}
              <EditButton onAction={handleEdit} />
            </h3>
          )}
          <div className="flex items-center gap-3">
            {localContact.dateOfBirth && (
              <span className="flex items-center gap-0.5 text-indigo-100 font-light text-sm">
                <FaBirthdayCake size={17} className="text-purple-400" />{" "}
                {new Date(localContact.dateOfBirth).toLocaleDateString()}
              </span>
            )}

            <LuArrowDownWideNarrow
              onClick={toggleAccordion}
              size={25}
              className={`rotate-0 transition-all ease-in duration-500 hover:text-pink-500 text-indigo-100 ${
                isOpen ? "rotate-180 text-pink-500" : ""
              }`}
            />
          </div>
        </div>
        {localContact.tags && (
          <TagSection
            contactId={contact.id}
            tags={localContact.tags}
            onUpdate={setLocalContact}
          />
        )}
      </div>

      <div
        className={`transition-(height) ease-in duration-500 overflow-hidden ${
          isOpen ? "max-h-200" : "max-h-0 "
        }`}>
        {localContact.emails && (
          <EmailSection
            contactId={contact.id}
            emails={localContact.emails}
            onUpdate={setLocalContact}
          />
        )}
        {localContact.phones && (
          <PhoneSection
            contactId={contact.id}
            phones={localContact.phones}
            onUpdate={setLocalContact}
          />
        )}
        {localContact.notes && (
          <NoteSection
            contactId={contact.id}
            notes={localContact.notes}
            onUpdate={setLocalContact}
          />
        )}
      </div>
    </div>
  );
};

export default ContactCard;
