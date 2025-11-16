import { useState } from "react";
import EditButton from "../Buttons/EditButton";
import { addPhone, updatePhone } from "../../api/api";
import EditableInput from "../Inputs/EditInput";
import AddButton from "../Buttons/AddButton";

interface Phone {
  id: number;
  phoneNumber: string;
}

interface PhoneSectionProps {
  contactId: number;
  phones: Phone[];
  onUpdate: (updater: (prev: any) => any) => void;
}

const validatePhoneNumber = (
  phone: string
): { isValid: boolean; error: string } => {
  const digitsOnly = phone.replace(/\D/g, "");
  if (digitsOnly.length !== 10) {
    return {
      isValid: false,
      error: "Phone number must contain exactly 10 digits",
    };
  }
  return { isValid: true, error: "" };
};

const PhoneSection = ({ contactId, phones, onUpdate }: PhoneSectionProps) => {
  const [addingPhone, setAddingPhone] = useState(false);
  const [newPhone, setNewPhone] = useState("");
  const [phoneError, setPhoneError] = useState("");
  const [editingPhoneId, setEditingPhoneId] = useState<number | null>(null);
  const [newPhoneNumber, setNewPhoneNumber] = useState("");
  const [editPhoneError, setEditPhoneError] = useState("");

  const handleAddPhone = () => {
    setAddingPhone(true);
    setPhoneError("");
  };

  const handleSaveNewPhone = async () => {
    const validation = validatePhoneNumber(newPhone);
    if (!validation.isValid) {
      setPhoneError(validation.error);
      return;
    }
    try {
      const newPhoneData = await addPhone(contactId, newPhone);
      onUpdate((prev) => ({
        ...prev,
        phones: [...prev.phones, newPhoneData],
      }));
      setAddingPhone(false);
      setNewPhone("");
      setPhoneError("");
    } catch (error) {
      console.error("Error adding phone:", error);
    }
  };

  const handleCancelNewPhone = () => {
    setAddingPhone(false);
    setNewPhone("");
    setPhoneError("");
  };

  const handleEditPhone = (phoneId: number, currentNumber: string) => {
    setEditingPhoneId(phoneId);
    setNewPhoneNumber(currentNumber);
    setEditPhoneError("");
  };

  const handleSavePhone = async () => {
    if (editingPhoneId === null) return;
    const validation = validatePhoneNumber(newPhoneNumber);
    if (!validation.isValid) {
      setEditPhoneError(validation.error);
      return;
    }
    try {
      await updatePhone(contactId, editingPhoneId, newPhoneNumber);
      onUpdate((prev) => ({
        ...prev,
        phones: prev.phones.map((phone: Phone) =>
          phone.id === editingPhoneId
            ? { ...phone, phoneNumber: newPhoneNumber }
            : phone
        ),
      }));
      setEditingPhoneId(null);
      setNewPhoneNumber("");
      setEditPhoneError("");
    } catch (error) {
      console.error("Error updating phone:", error);
    }
  };

  const handleCancelPhone = () => {
    setEditingPhoneId(null);
    setNewPhoneNumber("");
  };

  return (
    <div className="contact-section">
      <div className="flex justify-between items-center">
        <h4>Phones:</h4>
        {addingPhone ? (
          <p>
            <EditableInput
              value={newPhone}
              onChange={(value: string) => {
                setNewPhone(value);
                setPhoneError("");
              }}
              onSave={handleSaveNewPhone}
              onCancel={handleCancelNewPhone}
              className=""
            />
            {phoneError && (
              <span className="text-red-400 text-sm ml-2">{phoneError}</span>
            )}
          </p>
        ): <AddButton onAction={handleAddPhone} size={22} />}
        {/* <button
          onClick={handleAddPhone}
          className="bg-blue-500 text-white px-2 py-1 rounded text-sm hover:bg-blue-400">
          Add Phone
        </button> */}
      </div>
      <ul>
        {phones.map((phone) => (
          <li key={phone.id} className="flex items-center gap-2">
            {editingPhoneId === phone.id ? (
              <div className="flex flex-col gap-1">
                <EditableInput
                  value={newPhoneNumber}
                  onChange={(value: string) => {
                    setNewPhoneNumber(value);
                    setEditPhoneError("");
                  }}
                  onSave={handleSavePhone}
                  onCancel={handleCancelPhone}
                  className=""
                />
                {editPhoneError && (
                  <span className="text-red-400 text-sm ml-2">
                    {editPhoneError}
                  </span>
                )}
              </div>
            ) : (
              <>
                {phone.phoneNumber}
                <EditButton
                  onAction={() => handleEditPhone(phone.id, phone.phoneNumber)}
                />
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PhoneSection;
