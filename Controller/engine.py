# Standard library imports 
from typing import Any
from abc import ABC, abstractmethod
from dataclasses import dataclass

# Local application imports
from View.ui import UI
from Model.player import Player
from Model.story_pieces import Event
from Model.utils import decision_gen


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

def set_valid_action(action_dict:dict, options:list) -> None:
    decision = decision_gen()
    for value in options: 
        try:
            decision_letter = decision.__next__().name
        except StopIteration:
            break
        action_adder(action_dict, decision_letter, value)


@dataclass
class Engine(ABC):
    @abstractmethod
    def interact_with_player(ui: UI, player: Player, anything: Any) -> None:
        pass


@dataclass
class EventEngine(Engine):
    def interact_with_player(ui: UI, player: Player, event: Event) -> None:
        vaild_actions = {}
        set_valid_action(vaild_actions, event.options)
        
        outcomes = {}
        set_valid_action(outcomes, event.outcomes)

        ui.display_text(event.situation)
        while True:
            for key, option in remove_duplicates_keys(vaild_actions).items():
                ui.display_choose(key, option)

            player_input = ui.get_user_input()
            vaild_outcome = outcomes.get(player_input.lower(), None)
            if vaild_outcome:
                ui.display_text(vaild_outcome.result)
                vaild_outcome.modify_player(player)
                break
            else:
                ui.display_invalid_input(player_input)


@dataclass
class GameEngine(Engine):
    def interact_with_player(ui: UI, actions):
        for act in remove_duplicates_keys(actions).keys():
            ui.display_choose(act, "")
        player_input = ui.get_user_input()
        vaild_action = actions.get(player_input.lower())
        if vaild_action:
            vaild_action()
        else:
            ui.display_invalid_input(player_input)