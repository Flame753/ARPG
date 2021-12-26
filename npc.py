from creatures import Humonoid
import items
from creatures import Humonoid


class NonPlayableCharacter():
    def __init__(self) -> None:
        raise NotImplementedError("Do not creat raw NPC objects.")

    def __str__(self) -> str:
        return self.name

class Trader(NonPlayableCharacter, Humonoid):
    def __init__(self) -> None:
        self.name = "Trader"
        self.gold = 100
        
        starting_equipment = {items.Bread(): 4,
                            items.HealingPotion(): 2}
        self.add_items(starting_equipment)


                            