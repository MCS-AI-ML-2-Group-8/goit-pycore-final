from data.database import database_engine
from cli.messages import print_assistant_message, print_status_message
from cli.abstractions import CommandHandler, Result
from cli.contact_commands import ContactCommandHandlers
from cli.phone_commands import PhoneCommandHandlers
from cli.email_commands import EmailCommandHandlers
from cli.birthday_commands import BirthdayCommandHandlers
from cli.note_commands import NoteCommandHandlers
from cli.pipeline import execute_handler
from cli.completion import build_completer, build_auto_suggest
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings
from pathlib import Path
import shlex

def parse_input(user_input: str) -> tuple[str, list[str]]:
    if not user_input:
        return "", []
    try:
        parts = shlex.split(user_input, posix=True)
    except ValueError:
        parts = user_input.split()
    cmd = (parts[0].strip().lower() if parts else "")
    args = parts[1:] if len(parts) > 1 else []
    return cmd, args

def launch_main_loop():
    handlers: dict[str, CommandHandler] = {
        **ContactCommandHandlers(database_engine).get_commands(),
        **PhoneCommandHandlers(database_engine).get_commands(),
        **EmailCommandHandlers(database_engine).get_commands(),
        **BirthdayCommandHandlers(database_engine).get_commands(),
        **NoteCommandHandlers(database_engine).get_commands()
    }

    commands = ["hello", *handlers.keys(), "close", "exit", "history-clear"]

    # prompt_toolkit: комплитер + автосуггест
    completer = build_completer(database_engine, commands)
    auto_suggest = build_auto_suggest(database_engine, commands)

    history_path = Path.home() / ".goit_cli_history"
    session = PromptSession(
        history=FileHistory(str(history_path)),
        completer=completer,
        auto_suggest=auto_suggest
    )

    # Key bindings (опционально): Enter — принять строку, Tab — меню, Right — принять inline-хвост
    kb = KeyBindings()

    print_assistant_message("Welcome to the assistant bot!")
    while True:
        try:
            user_input = session.prompt(
                "Enter a command: ",
                enable_history_search=True,  # ↑/↓ работает с фильтром также
                completer=completer,
                complete_while_typing=True,
                auto_suggest=auto_suggest,
                key_bindings=kb
            )

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

        elif command == "history-clear":
            try:
                history_path.unlink(missing_ok=True)
                session = PromptSession(
                    history=FileHistory(str(history_path)),
                    completer=completer,
                    auto_suggest=auto_suggest
                )

                print_status_message(Result.SUCCESS, "Command history cleared.")
            except Exception as e:
                print_status_message(Result.WARNING, f"Failed to clear history: {e}")
            continue

        elif command in handlers:
            handler = handlers[command]
            status, message = execute_handler(handler, args)
            print_status_message(status, message)

        else:
            print_status_message(Result.WARNING, f'Invalid command. Available commands: {", ".join(commands)}')
