import axios from "axios";

const API_URL = "http://0.0.0.0:8000"; 

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
