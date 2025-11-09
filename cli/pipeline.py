from pydantic import ValidationError
from cli.abstractions import CommandHandler, CommandResult, Result
from data.exceptions import AlreadyExistsError, DomainError, NotFoundError


def execute_handler(handler: CommandHandler, args: list[str]) -> CommandResult:
    """
    Executes command handler in a safe manner and handles generic exceptions
    """
    try:
        return handler(args)

    except ValidationError as e:
        return Result.WARNING, f"WARNING: Validation error. {e}"

    except NotFoundError:
        return Result.WARNING, "WARNING: Item not found"

    except AlreadyExistsError:
        return Result.WARNING, "WARNING: Item already exists"

    except DomainError as e:
        return Result.ERROR, f"ERROR: Unhandled domain error.\n{e}"

    except Exception as e:
        return Result.ERROR, f"ERROR: Unhandled exception.\n{e}"
