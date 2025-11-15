import { getContacts, deleteContact as apiDeleteContact } from "../../api/api";

export const deleteContactCommand = async (
  currentInput: string
): Promise<any[]> => {
  // Parse command: "delete contact [name]"
  const parts = currentInput.split(" ");
  const nameIndex = parts.indexOf("contact") + 1;

  if (nameIndex === 0 || parts.length !== nameIndex + 1) {
    return [
      {
        type: "bot",
        text: "Invalid command format. Use: delete contact [name]",
      },
    ];
  }

  const contactName = parts[nameIndex];

  if (!contactName) {
    return [
      {
        type: "bot",
        text: "Invalid command format. Use: delete contact [name]",
      },
    ];
  }

  try {
    // Find the contact by name
    const allContacts = await getContacts();
    const contacts = allContacts.filter(
      (c: any) => c.name.toLowerCase() === contactName.toLowerCase()
    );

    if (contacts.length === 0) {
      return [
        {
          type: "bot",
          text: `Contact "${contactName}" not found.`,
        },
      ];
    }

    if (contacts.length > 1) {
      return [
        {
          type: "bot",
          text: `Found ${contacts.length} contacts with name "${contactName}":`,
        },
        { type: "bot", contacts: contacts },
        {
          type: "bot",
          text: "Please be more specific with the contact name.",
        },
      ];
    }

    // Delete the contact
    await apiDeleteContact(contacts[0].id);

    return [
      {
        type: "bot",
        text: `Successfully deleted contact "${contactName}".`,
      },
    ];
  } catch (error: any) {
    return [
      {
        type: "bot",
        text: `Error deleting contact: ${error.message}`,
      },
    ];
  }
};
