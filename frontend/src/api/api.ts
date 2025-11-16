import axios from "axios";

const API_URL = "https://magic-8.azurewebsites.net";

export const getContacts = async (name?: string) => {
  try {
    const url = name
      ? `${API_URL}/contacts?query=${name}`
      : `${API_URL}/contacts`;
    const response = await axios.get(url);
    return response.data;
  } catch (error) {
    console.error("Error fetching contacts:", error);
    throw error;
  }
};

export const getContactById = async (id: number) => {
  try {
    const response = await axios.get(`${API_URL}/contacts/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching contact with id ${id}:`, error);
    throw error;
  }
};

export const updatePhone = async (
  contactId: number,
  phoneId: number,
  newPhoneNumber: string
) => {
  try {
    const response = await axios.put(
      `${API_URL}/contacts/${contactId}/phones/${phoneId}`,
      {
        phone_number: newPhoneNumber,
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error updating phone:", error);
    throw error;
  }
};

export const addContact = async (contactData: {
  name: string;
  phone_number: string;
  date_of_birth: string | null;
}) => {
  try {
    const response = await axios.post(`${API_URL}/contacts`, contactData);
    return response.data;
  } catch (error) {
    console.error("Error adding contact:", error);
    throw error;
  }
};

export const deleteContact = async (contactId: number) => {
  try {
    const response = await axios.delete(`${API_URL}/contacts/${contactId}`);
    return response.data;
  } catch (error) {
    console.error("Error deleting contact:", error);
    throw error;
  }
};

export const updateContact = async (
  contactId: number,
  updateData: { name?: string; date_of_birth?: string | null }
) => {
  try {
    const response = await axios.put(
      `${API_URL}/contacts/${contactId}`,
      updateData
    );
    return response.data;
  } catch (error) {
    console.error("Error updating contact:", error);
    throw error;
  }
};

export const sendMesageToChat = async (text: string) => {
  const response = await axios.post(`${API_URL}/chat`, { text });
  return response.data as string[];
};


export const updateEmail = async (
  contactId: number,
  emailId: number,
  newEmailAddress: string
) => {
  try {
    const response = await axios.put(
      `${API_URL}/contacts/${contactId}/emails/${emailId}`,
      {
        email_address: newEmailAddress,
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error updating email:", error);
    throw error;
  }
};

export const addEmail = async (contactId: number, emailAddress: string) => {
  try {
    const response = await axios.post(
      `${API_URL}/contacts/${contactId}/emails`,
      {
        email_address: emailAddress,
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error adding email:", error);
    throw error;
  }
};

export const addPhone = async (contactId: number, phoneNumber: string) => {
  try {
    const response = await axios.post(
      `${API_URL}/contacts/${contactId}/phones`,
      {
        phone_number: phoneNumber,
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error adding phone:", error);
    throw error;
  }
};

export const updateNote = async (noteId: number, newText: string) => {
  try {
    const data: any = {
      text: newText,
    };
    console.log("Data:", data);
    const response = await axios.put(`${API_URL}/notes/${noteId}`, data);
    return response.data;
  } catch (error) {
    console.error("Error updating note:", error);
    throw error;
  }
};

export const addNote = async (contactId: number, text: string) => {
  try {
    const data: any = {
      text: text,
    };

    const response = await axios.post(
      `${API_URL}/contacts/${contactId}/notes`,
      data
    );
    return response.data;
  } catch (error) {
    console.error("Error adding note:", error);
    throw error;
  }
};

export const addContactTag = async (contactId: number, tag: string) => {
  try {
    const response = await axios.post(
      `${API_URL}/contacts/${contactId}/tags`,
      {
        label: tag,
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error adding tag:", error);
    throw error;
  }
};

export const deleteContactTag = async (contactId: number, tag: string) => {
  try {
    const response = await axios.delete(`${API_URL}/contacts/${contactId}/tags`, {
      data: {
        label: tag
      }
    });
    return response.data;
  } catch (error) {
    console.error("Error deleting tag:", error);
    throw error;
  }
};

export const addTagToNote = async ( noteId: number, tag: string) => {
  try {
    const response = await axios.post(
      `${API_URL}/notes/${noteId}/tags`,
      {
        label: tag,
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error adding tag to note:", error);
    throw error;
  }
};
