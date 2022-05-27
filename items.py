# Standard library imports  
from dataclasses import dataclass, field
import enum

# Local application imports
from utils import Dice


class BaseItem(enum.Enum):
    def __init__(self, cost: int, dice_type: Dice, amount: int) -> None:
        self.cost = cost
        self.dice_type = dice_type
        self.amount = amount
        

class Weapon(BaseItem):
    Rock = (1, Dice.d2, 1)
    Dagger = (10, Dice.d4, 1)
    Sword = (30, Dice.d6, 1)
    Crossbow = (45, Dice.d8, 1)
    Axe = (35, Dice.d8, 1)

    @property
    def damage(self) -> int:
        return self.dice_type.roll(self.amount)


class Consumable(BaseItem):
    Bread = (12, Dice.d4, 1)
    HealingPotion = (600, Dice.d4, 4)

    @property
    def healing(self) -> int:
        return self.dice_type.roll(self.amount)
