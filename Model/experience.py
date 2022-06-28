# Standard library imports 
from dataclasses import dataclass, field
from typing import Callable
from math import sqrt, floor
import enum



@dataclass
class Algorithm:
    formula: Callable
    reverse: Callable


class Algorithms(enum.Enum):
    Stats = Algorithm(formula = lambda x: 3 * (x ** 2), reverse = lambda x: sqrt(x / 3))
    Creature = Algorithm(formula = lambda x: 55 * (x ** 3), reverse = lambda x: (x/55)**(1/3))



@dataclass
class Level:
    algorithm: Algorithm
    xp: int = field(default=0, repr=False, init=False)

    def add_xp(self, num: int = 0):
        self.xp += num
    
    def subtrack_xp(self, num: int = 0):
        self.xp -= num
    
    def amount_to_next_level(self) -> int:
        level = self.get_level()
        next_levels_xp = self.algorithm.formula(level + 1)
        return next_levels_xp - self.xp

    def get_level(self) -> int:
        return floor(self.algorithm.reverse(self.xp))


# f = lambda x: 3 * (x ** 2) 
# for x in range(0, 201):
#     print(x, ": ", f(x))