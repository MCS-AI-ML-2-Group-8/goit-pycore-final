import { sendMesageToThread } from "../api/api"

export const sendMesage = async (message: string, threadId: string) => {
  const messages = await sendMesageToThread(message, threadId);
  return messages.map(text => (
    {
      type: "bot",
      text: text
    }
  ))
};
