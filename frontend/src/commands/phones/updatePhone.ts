import { getContacts, getContactById, updatePhone } from "../../api/api";

export async function updatePhoneCommand(currentInput: string): Promise<any[]> {
  const parts = currentInput.split(" ");
  const nameIndex = parts.indexOf("for") + 1;
  const fromIndex = parts.indexOf("from");
  const toIndex = parts.indexOf("to");

  if (nameIndex === 0 || fromIndex === -1 || toIndex === -1) {
    const botMessage = {
      type: "bot",
      text: "Invalid command format. Use: update phone for [name] from [old phone] to [new phone]",
    };
    return [botMessage];
  }

  const contactName = parts.slice(nameIndex, fromIndex).join(" ");
  const oldPhone = parts[fromIndex + 1];
  const newPhone = parts[toIndex + 1];

  if (!contactName.trim() || !oldPhone || !newPhone) {
    const botMessage = {
      type: "bot",
      text: "Invalid command format. Use: update phone for [name] from [old phone] to [new phone]",
    };
    return [botMessage];
  }

  try {
    // 1. Find the contact by name
    const allContacts = await getContacts();
    const contacts = allContacts.filter(
      (c: any) => c.name.toLowerCase() === contactName.toLowerCase()
    );

    if (contacts.length === 0) {
      const botMessage = {
        type: "bot",
        text: `Contact "${contactName}" not found.`,
      };
      return [botMessage];
    }
    if (contacts.length > 2) {
      const botMessage = {
        type: "bot",
        text: `Multiple contacts found for "${contactName}". Please be more specific.`,
      };
      return [botMessage];
    }
    const contact = contacts[0];

    // Find the phone to update
    const phoneToUpdate = contact.phones.find(
      (p: any) => p.phoneNumber === oldPhone
    );
    if (!phoneToUpdate) {
      const botMessage = {
        type: "bot",
        text: `Phone number "${oldPhone}" not found for ${contactName}.`,
      };
      return [botMessage];
    }

    await updatePhone(contact.id, phoneToUpdate.id, newPhone);

    const freshContact = await getContactById(contact.id);
    const updatedCardMessage = { type: "bot", contacts: [freshContact] };
    const confirmationMessage = {
      type: "bot",
      text: `Successfully updated phone for ${contactName}.`,
    };
    return [updatedCardMessage, confirmationMessage];
  } catch (error: any) {
    const errorMessage = {
      type: "bot",
      text: `Error updating phone: ${error.message}`,
    };
    return [errorMessage];
  }
}
