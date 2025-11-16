// EmailSection.tsx
import { useState } from "react";
import EditButton from "../Buttons/EditButton";
import { addEmail, updateEmail } from "../../api/api";
import EditableInput from "../Inputs/EditInput";
import AddButton from "../Buttons/AddButton";

interface Email {
  id: number;
  emailAddress: string;
}

interface EmailSectionProps {
  contactId: number;
  emails: Email[];
  onUpdate: (updater: (prev: any) => any) => void;
}

const EmailSection = ({ contactId, emails, onUpdate }: EmailSectionProps) => {
  const [addingEmail, setAddingEmail] = useState(false);
  const [newEmail, setNewEmail] = useState("");
  const [editingEmailId, setEditingEmailId] = useState<number | null>(null);
  const [newEmailAddress, setNewEmailAddress] = useState("");

  const handleAddEmail = () => {
    setAddingEmail(true);
  };

  const handleSaveNewEmail = async () => {
    try {
      const newEmailData = await addEmail(contactId, newEmail);
      onUpdate((prev) => ({
        ...prev,
        emails: [...prev.emails, newEmailData],
      }));
      setAddingEmail(false);
      setNewEmail("");
    } catch (error) {
      console.error("Error adding email:", error);
    }
  };

  const handleCancelNewEmail = () => {
    setAddingEmail(false);
    setNewEmail("");
  };

  const handleEditEmail = (emailId: number, currentAddress: string) => {
    setEditingEmailId(emailId);
    setNewEmailAddress(currentAddress);
  };

  const handleSaveEmail = async () => {
    if (editingEmailId === null) return;
    try {
      await updateEmail(contactId, editingEmailId, newEmailAddress);
      onUpdate((prev) => ({
        ...prev,
        emails: prev.emails.map((email: Email) =>
          email.id === editingEmailId
            ? { ...email, emailAddress: newEmailAddress }
            : email
        ),
      }));
      setEditingEmailId(null);
      setNewEmailAddress("");
    } catch (error) {
      console.error("Error updating email:", error);
    }
  };

  const handleCancelEmail = () => {
    setEditingEmailId(null);
    setNewEmailAddress("");
  };

  return (
    <div className="contact-section">
      <div className="flex justify-between items-center">
        <h4>Emails:</h4>
          {addingEmail ? (
          <p className="flex items-center gap-2">
            <EditableInput
              value={newEmail}
              onChange={setNewEmail}
              onSave={handleSaveNewEmail}
              onCancel={handleCancelNewEmail}
            />
          </p>
        ) : (
          <p><AddButton onAction={handleAddEmail} size={22}/></p>
        )}
      </div>
      <ul>
        {emails.map((email) => (
          <li key={email.id} className="flex items-center gap-2">
            {editingEmailId === email.id ? (
              <EditableInput
                value={newEmailAddress}
                onChange={setNewEmailAddress}
                onSave={handleSaveEmail}
                onCancel={handleCancelEmail}
              />
            ) : (
              <>
                {email.emailAddress}
                <EditButton
                  onAction={() => handleEditEmail(email.id, email.emailAddress)}
                />
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default EmailSection;
