# Standard library imports
from typing import Any

# Local application imports
from View.ui import UserInput, ValidActions


def action_adder(action_dict: dict, hotkey: str, action: Any) -> None:
    action_dict[hotkey.capitalize()] = action
    action_dict[hotkey.upper()] = action
    action_dict[hotkey.lower()] = action   

def remove_duplicates_keys(actions_dict: dict) -> dict:
    result = {}

    for key,value in actions_dict.items():
        if value not in result.values():
            result[key.lower()] = value

    return result


class CLI:
    def display_title(self, title: str) -> None:
        style = "*"*3
        print(style ,title, style, end="\n\n")
    
    def display_actions(self, actions: ValidActions) -> None:
        without_dup = remove_duplicates_keys(actions)
        for action in without_dup.keys():
            print(f"{action.capitalize()}: ")

    def get_user_input(self, input_text: str="Action") -> str:
        return input(f"{input_text}: ")
    
    def display_invalid_input(self, user_input: UserInput) -> None:
        print(f"Invalid Action! <{user_input}> Try again!\n")
    
    def display_text(self, text: str) -> None:
        print(text)

    def interact_with_user(self, actions: ValidActions) -> Any:
        while True:
            self.display_actions(actions)
            user_input = self.get_user_input()
            vaild_action = actions.get(user_input)
            if vaild_action:
                return vaild_action
            else:
                self.display_invalid_input(user_input=user_input)
