from dataclasses import dataclass, field
from items import BaseItem
import slots
import setting


@dataclass() 
class Creature():
    def __init__(self):
        self.inventory = slots.Miscellaneous()
        self.coin_pouch = slots.Coins()
        self.helmet = slots.Head()
        self.chest = slots.Body()
        self.legs = slots.Legs()
        self.boots = slots.Boots()
        self.one_handed = slots.OneHanded()
        self.two_handed = slots.TwoHanded()


    def _verifyArguments(self, item=None, amount=None):
        # Verifys if Arguments are enter correctly 
        if item:
            if not isinstance(item, BaseItem):
                raise TypeError(f'The item argument requires to be a BaseItem Object, not a {type(item)}!')
        if amount:
            if not type(amount) == int:
                raise TypeError(f'The amount argurment requires to be a intger, not a {type(amount)}!')
            if amount < 0:
                raise ValueError("The amount argurment can't be an negative real number!")
        if type(item) in [list, dict, tuple] or type(amount) in [list, dict, tuple]:
            raise TypeError(f"Arguments can't be a empty List, Dictionary or Tuple")

    def addItem(self, item: BaseItem, amount: int=1):
        self._verifyArguments(item, amount)

        # Always adds the amount of items into the invenotry slot excluding any Coin items
        if item.slot_type == setting.COIN_SLOT:
            self.coin_pouch.addItem(item, amount)
        else:
            self.inventory.addItem(item, amount)

    def removeItem(self, item: BaseItem, amount: int=1) -> bool:
        self._verifyArguments(item, amount)

        if item.slot_type == setting.COIN_SLOT:
            return self.coin_pouch.removeItem(item, amount)
        else:
            return self.inventory.removeItem(item, amount)

    def equip(self, item: BaseItem) -> bool:
        self._verifyArguments(item)
        # Verifying if there is an item to equip
        if not item in self.inventory.items:
            # No items to equip
            return False
        for slot in self.__dict__.values():
            # Finds proper slot for item
            if slot.type == item.slot_type:
                try:
                    # Adds item and checks if item was added
                    slot.addItem(item, 1)
                    return True
                except IndexError:
                    # Capacity was reached
                    return False

    def unequip(self, item: BaseItem) -> bool:
        self._verifyArguments(item)

        for slot in self.__dict__.values():
            # Slots to Ignore 
            if slot.type in [setting.MISC_SLOT, setting.COIN_SLOT]: continue
            if slot.type == item.slot_type:
                # perventing any new/more items to be added if there was no items remove
                if slot.removeItem(item, 1):
                    return True
        return False
    
    def calculateItemWorth(self, item):
        self._verifyArguments(item)

        if item.slot_type == setting.COIN_SLOT:
            return self.coin_pouch.calculateItemWorth(item)
        else:
            return self.inventory.calculateItemWorth(item)

    def calculateTotalWorth(self) -> int:
        return self.coin_pouch.calculateTotalWorth() + self.inventory.calculateTotalWorth()

    def is_alive(self) -> bool:
        return self.hp > 0
  



def main():
    import items
    h = Creature()

    d = items.Dagger()
    b = items.Bread()




if __name__ == '__main__':
    pass