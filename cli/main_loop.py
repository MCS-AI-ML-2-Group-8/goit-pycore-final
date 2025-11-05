from cli.database import database_engine
from cli.messages import print_assistant_message, print_status_message
from cli.abstractions import CommandHandler, Result
from cli.contact_commands import ContactCommandHandlers
from cli.phone_commands import PhoneCommandHandlers

def parse_input(user_input: str) -> tuple[str, list[str]]:
    if not user_input:
        return "", []

    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def launch_main_loop():
    handlers: dict[str, CommandHandler] = {
        **ContactCommandHandlers(database_engine).get_commands(),
        **PhoneCommandHandlers(database_engine).get_commands()
    }

    commands = ["hello", *handlers.keys(), "close", "exit"]

    print_assistant_message("Welcome to the assistant bot!")
    while True:
        try:
            user_input = input("Enter a command: ")

        except KeyboardInterrupt:
            print("Keyboard interrupt")
            print_assistant_message("Ok, bye!")
            break

        command, args = parse_input(user_input)
        if command in ["exit", "close"]:
            print_assistant_message("Good bye!")
            break

        elif command == "hello":
            print_assistant_message("How can I help you?")

        elif command in handlers:
            handler = handlers[command]
            status, message = handler(args)
            print_status_message(status, message)

        else:
            print_status_message(Result.WARNING, f"Invalid command. Available commands: {", ".join(commands)}")
