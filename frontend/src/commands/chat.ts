import { sendMesageToChat } from "../api/api"

export const sendMesage = async (message: string) => {
  const messages = await sendMesageToChat(message);
  return messages.map(text => (
    {
      type: "bot",
      text: text
    }
  ))
};
