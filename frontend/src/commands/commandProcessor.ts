import {
  getAllContactsCommand,
  getOneContactByIdCommand,
} from "./contacts/getContacts";

import { addContactCommand } from "./contacts/addContact";
import { deleteContactCommand } from "./contacts/deleteContact";
import { updateContactCommand } from "./contacts/updateContact";
import { helpCommand } from "./help";
import { sendMesage } from "./chat";

export async function processCommand(currentInput: string, threadId: string) {
  const input = currentInput.trim().toLowerCase();

  const simulateTyping = () =>
    new Promise((resolve) => setTimeout(resolve, 1500 + Math.random() * 1000));

  // Command: help
  if (input === "help") {
    const helpMessages = await helpCommand();
    await simulateTyping();
    return helpMessages;
  }

  // Command: hi/hello/help
  else if (input === "hi" || input === "hello") {
    const botMessage = {
      type: "bot",
      text: "Hi! How can I help you today? Type 'help' to see all available commands.",
    };
    await simulateTyping();
    return [botMessage];
  }

  // Command: exit, close, bye
  else if (input === "exit" || input === "close" || input === "bye") {
    const botMessage = {
      type: "bot",
      text: "👋 Goodbye! Thank you for using Magic Contact Bot.",
    };
    await simulateTyping();
    return [botMessage];
  }

  // Command: get-contacts
  else if (input === "get contacts") {
    const botMessage = await getAllContactsCommand();
    return botMessage;
  } else if (currentInput.toLowerCase().startsWith("get contact")) {
    const botMessage = await getOneContactByIdCommand(input);
    await simulateTyping();
    return botMessage;
  }

  // Command: add contact [name] [phone] [birth_date]
  else if (currentInput.toLowerCase().startsWith("add contact")) {
    const addMessages = await addContactCommand(currentInput);
    await simulateTyping();
    return addMessages;
  }

  // Command: delete contact [name]
  else if (currentInput.toLowerCase().startsWith("delete contact")) {
    const deleteMessages = await deleteContactCommand(currentInput);
    await simulateTyping();
    return deleteMessages;
  }

  // Command: update contact [name] to [new_name] birthday [date] (birthday is optional)
  else if (currentInput.toLowerCase().startsWith("update contact")) {
    const updateMessages = await updateContactCommand(currentInput);
    await simulateTyping();
    return updateMessages;
  } else {
    return await sendMesage(currentInput, threadId);
  }
}
