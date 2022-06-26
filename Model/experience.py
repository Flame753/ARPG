# Standard library imports 
from dataclasses import dataclass
from typing import Callable
from math import sqrt, floor

@dataclass
class Level:
    xp: int = 0
    algorithm: Callable = lambda x: sqrt(x/3)

    def add_xp(self, num: int = 0):
        self.xp += num
    
    def subtrack_xp(self, num: int = 0):
        self.xp -= num

    def get_level(self) -> int:
        return floor(self.algorithm(self.xp))


# f = lambda x: 3 * (x ** 2) 
# for x in range(0, 201):
#     print(x, ": ", f(x))