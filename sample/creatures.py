from dataclasses import dataclass, field
from items import BaseItem
import slots
import setting
from pprint import pprint


class EquippedItemRemovealError(Exception):
    """Exception raised for not unequipped existing item before removing the item."""
    
    def __init__(self, message="Item was attempted to be removed, before being unequipped!"):
        self.message = message
        super().__init__(self.message)

# class UnequippableError(Exception):
#     """Exception raised for attempting to equip or unequip an item to a unequippable slot."""
    
#     def __init__(self, message="test g"):
#         self.message = message
#         super().__init__(self.message)


def _isSlotEquippable(slot: slots.Slot) -> bool:
    return True if slot.item_limit else False
    


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

        if self._isItemEquipped(item): raise EquippedItemRemovealError

        if item.slot_type == setting.COIN_SLOT:
            return self.coin_pouch.removeItem(item, amount)
        else:
            return self.inventory.removeItem(item, amount)

    def equip(self, item: BaseItem) -> bool:
        self._verifyArguments(item)

        if not item in self.inventory.container: return False # No items to equip
        if not self._locateSlot(item): return False
        if not _isSlotEquippable(self._locateSlot(item)): return False
        try:
            # Adds item and checks if item was added
            self._locateSlot(item).addItem(item, 1)
            return True
        except slots.CapacityReachedError:
            # Capacity was reached
            return False

    def unequip(self, item: BaseItem) -> bool:
        self._verifyArguments(item)

        if not self._locateSlot(item): return False
        if not _isSlotEquippable(self._locateSlot(item)): return False
        return True if self._locateSlot(item).removeItem(item, 1) else False

    def _isItemEquipped(self, item: BaseItem) -> bool:
        if not self._locateSlot(item): return False
        if not _isSlotEquippable(self._locateSlot(item)): return False
        return True if item in self._locateSlot(item).container else False
    
    def _locateSlot(self, item: BaseItem) -> slots.Slot:
        for slot in self.__dict__.values():
            if not isinstance(slot, slots.Slot):continue
            if slot.type != item.slot_type: continue
            return slot

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
    c = Creature()

    d = items.Dagger()
    b = items.Bread()
    c.addItem(b)
    # print(c.equip(b))
    # print(c.inventory.container)
    # print(c.unequip(b))
    # print(b.slot_type)

    print(_isSlotEquippable(slots.Miscellaneous()))
    print(_isSlotEquippable(slots.Coins()))
    print(_isSlotEquippable(slots.Head()))



if __name__ == '__main__':
    main()