# Standard library imports

# Local application imports
from View.ui import UserInput, ValidActions
from typing import Any
import Model.utils as utils


class CLI:
    def display_title(self, title: str) -> None:
        style = "*"*3
        print(style ,title, style, end="\n\n")
    
    def display_actions(self, actions: ValidActions) -> None:
        without_dup = utils.remove_duplicates_keys(actions)
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


# from utils import action_adder
# c = CLI()
# # print(c.interact_with_user({"A": "you got it"}))
# dic = {}
# action_adder(dic, "A", "b")
# action_adder(dic, "As", "d")
# action_adder(dic, "A", "c")
# action_adder(dic, "Time", "z")
# action_adder(dic, "Create", "e")
# print(dic)
# # c.display_actions(actions=dic)
# print(c.interact_with_user(dic))

