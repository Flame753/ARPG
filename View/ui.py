# Standard library imports  
from typing import Protocol


class UI(Protocol):
    def display_title(self, title: str) -> None:
        raise NotImplementedError()

    def display_choose(self, option: str, text: str) -> None:
        raise NotImplementedError()

    def get_user_input(self, input_text: str="Action") -> str:
        raise NotImplementedError()

    def display_invalid_input(self, user_input: str) -> None:
        raise NotImplementedError()

    def display_text(self, text: str) -> None:
        raise NotImplementedError()
