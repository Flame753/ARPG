from dataclasses import dataclass, field
from items import BaseItem
import slots
import setting


@dataclass() 
class Creature():
    def __init__(self):
        self.inventory = slots.Inventory()

    # def getAllItems(self) -> tuple[BaseItem, dict]:
    #     items = {}

    #     for data in self.misc.values():
    #         slot = data['slot']
    #         items.update(slot.misc)
    #     return items.items()

    def is_alive(self) -> bool:
        return self.hp > 0
  



def main():
    import items
    h = Creature()

    d = items.Dagger()
    b = items.Bread()




if __name__ == '__main__':
    pass