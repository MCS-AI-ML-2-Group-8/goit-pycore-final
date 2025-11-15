import { getContacts, getContactById } from "../../api/api";

//  get all contacts
export const getAllContactsCommand = async () => {
  try {
    const contactsData = await getContacts();
    return [{ type: "bot", contacts: contactsData }];
  } catch (error: any) {
    return [{ type: "bot", text: `Error: ${error.message}` }];
  }
};

// get a contacts by ID
export const getOneContactByIdCommand = async (currentInput: string) => {
  try {
    const parts = currentInput.split(" ");
    const contactNameIdx = parts.indexOf("contact") + 1;
    const contactName = parts[contactNameIdx];

    if (!contactName) {
      return [
        {
          type: "bot",
          text: "Please specify a contact name. Usage: get contact [name]",
        },
      ];
    }

    const allContacts = await getContacts();
    const contacts = allContacts.filter(
      (c: any) => c.name.toLowerCase() === contactName.toLowerCase()
    );

    if (contacts.length === 0) {
      return [{ type: "bot", text: `Contact "${contactName}" not found.` }];
    } else if (contacts.length > 1) {
      return [
        {
          type: "bot",
          text: `Found ${contacts.length} contacts with name "${contactName}":`,
        },
        { type: "bot", contacts: contacts },
      ];
    } else {
      const contactData = await getContactById(contacts[0].id);
      return [{ type: "bot", contacts: [contactData] }];
    }
  } catch (error: any) {
    return [{ type: "bot", text: `Error: ${error.message}` }];
  }
};
