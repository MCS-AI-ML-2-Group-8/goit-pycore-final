from enum import Enum
from typing import Callable


class Result(Enum):
    """
    Possible command handler result statuses
    """
    SUCCESS = 0
    SUCCESS_DATA = 1
    WARNING = 2
    ERROR = 3


CommandHandler = Callable[
    [list[str]],
    tuple[Result, str]
]
