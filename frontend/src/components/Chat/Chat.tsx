import { useState, useEffect, useRef } from "react";
import FloatingIcons from "./FloatingIcons";
import ContactCard from "../ContactCard/ContactCard";

import { processCommand } from "../../commands/commandProcessor";

export function Chat() {
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [messages, setMessages] = useState<any[]>([
    {
      type: "bot",
      text: "Hello! I am your contact assistant. How can I help you? Type 'help' to see all avalaible commands.",
    },
  ]);

  // smooth scrolling
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // input handler
  const handleSend = async () => {
    if (input.trim() === "") return;

    const userMessage = { type: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);

    const currentInput = input;
    setInput("");

    //   simulate typing
    setIsTyping(true);
    await new Promise((resolve) =>
      setTimeout(resolve, 1500 + Math.random() * 1000)
    );

    const botMessages = await processCommand(currentInput);
    setIsTyping(false);
      
    setMessages((prev) => [...prev, ...botMessages]);
  };
    

  return (
    <>
      <FloatingIcons />
      <div className="w-full max-w-3xl h-[90vh] flex flex-col bg-gray-900/80 backdrop-blur-sm rounded-2xl shadow-2xl overflow-hidden z-10">
        {/* Header */}
        <div className="p-4 border-b border-gray-700 bg-linear-to-r from-purple-900 via-rose-900 to-purple-900">
          <div className="flex items-center justify-center space-x-3">
            <h1 className="text-2xl font-bold text-center text-white">
              Magic Contact Bot
            </h1>
          </div>
        </div>

        {/* Messages*/}
        <div className="flex-1 p-6 space-y-4 overflow-y-auto">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${
                msg.type === "user" ? "justify-end" : "justify-start"
              }`}>
              {msg.contacts ? (
                <div className="w-full">
                  {msg.contacts.map((contact: any) => (
                    <ContactCard key={contact.id} contact={contact} />
                  ))}
                </div>
              ) : (
                <div
                  className={`py-2 px-4 rounded-2xl max-w-lg ${
                    msg.type === "user"
                      ? "bg-linear-to-r from-fuchsia-500 to-fuchsia-600 text-white"
                      : "bg-linear-to-r from-purple-300 to-indigo-200"
                  } ${msg.type === "bot" ? "whitespace-pre-line" : ""}`}>
                  {msg.text}
                </div>
              )}
            </div>
          ))}
          {isTyping && (
            <div className="flex justify-start">
              <div className="py-3 px-4 rounded-2xl bg-linear-to-r from-purple-300 to-indigo-200">
                <div className="flex items-center space-x-3">
                  <img
                    src="/logo.png"
                    alt="Bot typing"
                    className="w-6 h-6 animate-spin"
                    style={{ animationDuration: "1s" }}
                  />
                  <span className="text-sm text-gray-700 font-medium">
                    Bot is typing...
                  </span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 border-t border-gray-700">
          <div className="flex items-center bg-gray-800 rounded-xl p-2">
            <input
              type="text"
              className="flex-1 bg-transparent text-white px-4 focus:outline-none"
              placeholder="Type 'get-contacts'..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyUp={(e) => e.key === "Enter" && handleSend()}
            />
            <button
              onClick={handleSend}
              className="bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700">
              Send
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
