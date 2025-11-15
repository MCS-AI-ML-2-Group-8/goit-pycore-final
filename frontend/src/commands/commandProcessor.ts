import {
  getAllContactsCommand,
  getOneContactByIdCommand,
} from "./contacts/getContacts";
import { updatePhoneCommand } from "./phones/updatePhone";
import { addContactCommand } from "./contacts/addContact";
import { deleteContactCommand } from "./contacts/deleteContact";
import { updateContactCommand } from "./contacts/updateContact";
import { helpCommand } from "./help";

export async function processCommand(currentInput: string) {
  const input = currentInput.trim().toLowerCase();

  // Command: help
  if (input === "help") {
    const helpMessages = await helpCommand();
    return helpMessages;
  }

  // Command: hi/hello/help
  if (input === "hi" || input === "hello") {
    const botMessage = {
      type: "bot",
      text: "Hi! How can I help you today? Type 'help' to see all available commands.",
    };
    return [botMessage];
  }

  // Command: exit, close, bye
  if (input === "exit" || input === "close" || input === "bye") {
    const botMessage = {
      type: "bot",
      text: "👋 Goodbye! Thank you for using Magic Contact Bot.",
    };
    return [botMessage];
  }

  // Command: get-contacts
  if (input === "get-contacts") {
    const botMessage = await getAllContactsCommand();
    return botMessage;
  }
  if (currentInput.toLowerCase().startsWith("get contact")) {
    const botMessage = await getOneContactByIdCommand(input);
    return botMessage;
  }

  // Command: update phone for [name] from [old phone] to [new phone]
  if (currentInput.toLowerCase().startsWith("update phone for")) {
    const updateMessages = await updatePhoneCommand(currentInput);
    return updateMessages;
  }

  // Command: add contact [name] [phone] [birth_date]
  if (currentInput.toLowerCase().startsWith("add contact")) {
    const addMessages = await addContactCommand(currentInput);
    return addMessages;
  }

  // Command: delete contact [name]
  if (currentInput.toLowerCase().startsWith("delete contact")) {
    const deleteMessages = await deleteContactCommand(currentInput);
    return deleteMessages;
  }

  // Command: update contact [name] to [new_name] birthday [date] (birthday is optional)
  if (currentInput.toLowerCase().startsWith("update contact")) {
    const updateMessages = await updateContactCommand(currentInput);
    return updateMessages;
  }

  // Otherwise
  const botMessage = {
    type: "bot",
    text: `I'm sorry😢 I don't recognize the '${currentInput}' command. Type 'help' to see what I can do for you😊`,
  };
  return [botMessage];
}
