import { addContact } from "../../api/api";

export const addContactCommand = async (
  currentInput: string
): Promise<any[]> => {
  // Parse command: "add contact [name] [phone] [birth_date]" (birth_date is optional)
  const parts = currentInput.split(" ");
  const nameIndex = parts.indexOf("contact") + 1;

  if (nameIndex === 0 || parts.length < nameIndex + 2) {
    return [
      {
        type: "bot",
        text: "Invalid command format. Use: add contact [name] [phone_number] [date_of_birth - optional]",
      },
    ];
  }

  const name = parts[nameIndex];
  const phoneNumber = parts[nameIndex + 1];
  const dateOfBirth =
    parts.length > nameIndex + 2 ? parts[nameIndex + 2] : null;

  if (!name || !phoneNumber) {
    return [
      {
        type: "bot",
        text: "Invalid command format. Use: add contact [name] [phone_number] [date_of_birth - optional]",
      },
    ];
  }

  // Validate date format if provided (basic validation)
  if (dateOfBirth) {
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!dateRegex.test(dateOfBirth)) {
      return [
        {
          type: "bot",
          text: "Invalid date format. Use YYYY-MM-DD format for date of birth.",
        },
      ];
    }
  }

  try {
    const contactData: {
      name: string;
      phone_number: string;
      date_of_birth: string | null;
    } = {
      name: name,
      phone_number: phoneNumber,
      date_of_birth: dateOfBirth || null,
    };

    const newContact = await addContact(contactData);

    return [
      { type: "bot", contacts: [newContact] },
      {
        type: "bot",
        text: `Successfully added contact '${name}'.`,
      },
    ];
  } catch (error: any) {
    // Handle specific error cases
    if (error.response?.status === 400) {
      return [
        {
          type: "bot",
          text: `${error.response?.data.detail.message}:'${name}'`,
        },
      ];
    }

    return [
      {
        type: "bot",
        text: `Error adding contact: ${error.message}`,
      },
    ];
  }
};
