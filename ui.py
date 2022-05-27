# Standard library imports  
from typing import Protocol, Callable, TypeVar, Any

# Local application imports


# Type Hints
UserInput = TypeVar("UserInput")
ValidActions = dict[str, Any]


class UI(Protocol):
    def display_title(self, title: str) -> None:
        raise NotImplementedError()

    def display_actions(self, actions: ValidActions) -> None:
        raise NotImplementedError()

    def get_user_input(self, input_text: str="Action") -> UserInput:
        raise NotImplementedError()

    def display_invalid_input(self, user_input: UserInput) -> None:
        raise NotImplementedError()

    def display_text(self, text: str) -> None:
        raise NotImplementedError()

    def interact_with_user(self, actions: ValidActions) -> Any:
        raise NotImplementedError()
