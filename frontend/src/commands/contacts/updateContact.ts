import {
  getContacts,
  getContactById,
  updateContact as apiUpdateContact,
} from "../../api/api";

export const updateContactCommand = async (
  currentInput: string
): Promise<any[]> => {
  // Parse command: "update contact [current_name] to [new_name] birthday [new_date]" (birthday is optional)
  const parts = currentInput.split(" ");
  const contactIndex = parts.indexOf("contact") + 1;

  if (contactIndex === 0 || parts.length < contactIndex + 3) {
    return [
      {
        type: "bot",
        text: "Invalid command format. Use: update contact [name] to [new_name] birthday [YYYY-MM-DD] (birthday is optional)",
      },
    ];
  }

  const contactName = parts[contactIndex];
  const toIndex = parts.indexOf("to", contactIndex);

  if (!contactName || toIndex === -1 || toIndex + 1 >= parts.length) {
    return [
      {
        type: "bot",
        text: "Invalid command format. Use: update contact [name] to [new_name] birthday [YYYY-MM-DD] (birthday is optional)",
      },
    ];
  }

  const newName = parts[toIndex + 1];
  let newBirthday: string | null = null;

  // Check for optional birthday
  const birthdayIndex = parts.indexOf("birthday", toIndex);
  if (birthdayIndex !== -1 && birthdayIndex + 1 < parts.length) {
    newBirthday = parts[birthdayIndex + 1];
  }

  if (!newName) {
    return [
      {
        type: "bot",
        text: "New name is required. Use: update contact [name] to [new_name] birthday [YYYY-MM-DD] (birthday is optional)",
      },
    ];
  }

  // Validate date format if birthday is provided
  if (newBirthday) {
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!dateRegex.test(newBirthday)) {
      return [
        {
          type: "bot",
          text: "Invalid date format. Use YYYY-MM-DD format for birthday.",
        },
      ];
    }
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

    const contact = contacts[0];

    // If birthday not provided, keep existing birthday
    if (newBirthday === null && contact.dateOfBirth) {
      newBirthday = contact.dateOfBirth;
    }

    const updateData: { name: string; date_of_birth: string | null } = {
      name: newName,
      date_of_birth: newBirthday,
    };

    // Update the contact
    await apiUpdateContact(contact.id, updateData);

    // Get updated contact data
    const updatedContact = await getContactById(contact.id);

    return [
      { type: "bot", contacts: [updatedContact] },
      {
        type: "bot",
        text: `Successfully updated contact "${contactName}".`,
      },
    ];
  } catch (error: any) {
    return [
      {
        type: "bot",
        text: `Error updating contact: ${error.message}`,
      },
    ];
  }
};
