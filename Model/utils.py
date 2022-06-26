# Standard library imports  
from abc import ABC
from dataclasses import dataclass
from typing import Any
import enum
import random

# Local application imports


# ----------------------------------------------------------------------------------
def _verify_amount_arg(amount: int) -> None:
    if not isinstance(amount, int): raise TypeError
    if amount < 0: raise ValueError


@dataclass
class Container(ABC):
    def _ensure_inventory(self):
        if not hasattr(self, '_inventory'):
            self._inventory = dict()

    def get_all(self) -> dict:
        self._ensure_inventory()
        return self._inventory

    def add(self, obj: Any, amount: int = 0):
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

# ----------------------------------------------------------------------------------
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

# ----------------------------------------------------------------------------------
class Decision(enum.Enum):
    A = enum.auto()
    B = enum.auto()
    C = enum.auto()
    D = enum.auto()

def decision_gen():
    for d in Decision:
        yield d 

# ----------------------------------------------------------------------------------
class Color(enum.Enum):
    Red = "FF0000"
    Green = "00FF00"
    Blue = "0000FF"
    Black = "000000"
    White = "FFFFFF"

# ----------------------------------------------------------------------------------