from colorama import Fore
from cli.abstractions import Result


def print_assistant_message(message: str):
    print(f"{Fore.BLUE}{message}{Fore.RESET}")


def print_status_message(status: Result, message: str):
    if status == Result.SUCCESS:
        print(f"{Fore.GREEN}{message}{Fore.RESET}")

    elif status == Result.WARNING:
        print(f"{Fore.YELLOW}{message}{Fore.RESET}")

    elif status == Result.ERROR:
        print(f"{Fore.RED}{message}{Fore.RESET}")

    else:
        print(message)
