# Standard library imports  

# Local application imports
from utils import Container


class Player(Container):
    def __init__(self, name:str, hp:int = 10) -> None:
        self.name = name
        self.hp = hp

    def is_alive(self) -> bool:
        return self.hp > 0