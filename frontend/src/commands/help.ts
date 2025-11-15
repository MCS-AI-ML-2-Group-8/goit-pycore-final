export const helpCommand = async () => {
  return [
    {
      type: "bot",
      text: `🤖 Available Commands:

📋 CONTACT MANAGEMENT:
• get-contacts - Show all contacts
• get contact [name] - Find contact by name
• add contact [name] [phone] [birthday-optional] - Add new contact
Example: add contact John 1234567890 1990-01-01
• update contact [current_name] to [new_name] birthday [YYYY-MM-DD] - Update contact (birthday optional)
Example: update contact John to Johnny birthday 1990-01-01
• delete contact [name] - Delete contact
Example: delete contact John

📞 PHONE MANAGEMENT:
• update phone for [name] from [old_phone] to [new_phone] - Update phone number
Example: update phone for John from 1234567890 to 0987654321

🎯 SYSTEM COMMANDS:
• help - Show this help message
• hi/hello - Greeting
• exit/close/bye - Exit application

💡 TIPS:
• Names are case-sensitive
• Dates must be in YYYY-MM-DD format
• Phone numbers can contain only 10 numbers`,
    },
  ];
};
