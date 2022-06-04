# Standard library imports  
from abc import ABC
from typing import Any, Callable
from dataclasses import dataclass
import enum
import random
import itertools

# Local application imports


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



def _verify_amount_arg(amount: int) -> None:
    if not isinstance(amount, int): raise TypeError
    if amount < 0: raise ValueError


@dataclass
class Container(ABC):
    def _ensure_inventory(self) -> None:
        if not hasattr(self, '_inventory'):
            self._inventory = dict()

    def get_inventory(self):
        self._ensure_inventory()
        return self._inventory

    def add(self, obj: Any, amount: int = 0) -> None:
        self._ensure_inventory()
        _verify_amount_arg(amount)

        if obj in self._inventory:
            self._inventory[obj]['amount'] += amount
        else:
            self._inventory[obj] = {'amount': amount}

    def remove(self, obj: Any, amount: int = 0) -> bool:
        self._ensure_inventory()
        _verify_amount_arg(amount)

        if obj in self._inventory:
            if self._inventory[obj]['amount'] >= amount:
                self._inventory[obj]['amount'] -= amount
                if self._inventory[obj]['amount'] == 0:
                    del(self._inventory[obj])
                return True
        return False

    # def calculate_item_weight(self, obj) -> int:
    #     self._ensure_inventory()

    #     if obj in self._inventory:
    #         return obj.weight * self._inventory[obj]['amount']
    #     return 0

    # def calculate_item_worth(self, obj)  -> int:
    #     self._ensure_inventory()

    #     if obj in self._inventory:
    #         return obj.worth * self._inventory[obj]['amount']
    #     return 0

    # def calculate_total_weight(self) -> int:
    #     self._ensure_inventory()

    #     weight = 0
    #     for obj, data in self._inventory.items():
    #         weight += obj.weight * data['amount']
    #     return weight

    # def calculate_total_worth(self) -> int:
    #     self._ensure_inventory()

    #     worth = 0
    #     for obj, data in self._inventory.items():
    #         worth += obj.worth * data['amount']
    #     return worth


class Dice(enum.IntEnum):
    d2 = 2
    d4 = 4
    d6 = 6
    d8 = 8
    d10 = 10
    d12 = 12
    d20 = 20

    def roll(self, num_of_rolls: int=1) -> int:
        if num_of_rolls <= 0: raise ValueError("num_of_rolls requires to be a Positvie Integer!")
        return sum([random.randint(1, self.value) for _ in range(0, num_of_rolls)])

    @staticmethod
    def roll_all(lis_dice, num_of_rolls: int=1) -> int:
        return sum([dice.roll(num_of_rolls) for dice in lis_dice])


@dataclass
class DiceContainer(Container):
    def add(self, dice: Dice, amount: int = 0) -> None:
        if not isinstance(dice, Dice): raise 
        super().add(dice, amount)

    def remove(self, dice: Dice, amount: int = 0) -> bool:
        if not isinstance(dice, Dice): raise 
        super().remove(dice, amount)

