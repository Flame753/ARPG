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


# def _isSlotEquippable(slot: slots.Slot) -> bool:
#     return True if slot.item_limit else False
    


# @dataclass() 
class Creature():
    def __init__(self):
        self.inventory = slots.Miscellaneous()
        self.coin_pouch = slots.Coins()
        self.equippable_slots = slots.EquipmentSlots()


    def _verifyArguments(self, item: BaseItem=None, amount: int=None) -> None:
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

    def addItem(self, item: BaseItem, amount: int=1) -> None:
        self._verifyArguments(item, amount)

        # Always adds the amount of items into the invenotry slot excluding any Coin items
        if item.slot_type == setting.COIN_SLOT:
            self.coin_pouch.addItem(item, amount)
        else:
            self.inventory.addItem(item, amount)

    def removeItem(self, item: BaseItem, amount: int=1) -> bool:
        self._verifyArguments(item, amount)

        if self.equippable_slots.isItemEquipped(item): raise EquippedItemRemovealError

        if item.slot_type == setting.COIN_SLOT:
            return self.coin_pouch.removeItem(item, amount)
        else:
            return self.inventory.removeItem(item, amount)

    def equip(self, item: BaseItem) -> bool:
        self._verifyArguments(item)

        if not item in self.inventory.container: return False # No items to equip
        return self.equippable_slots.equip(item)

    def unequip(self, item: BaseItem) -> bool:
        self._verifyArguments(item)

        return True if self.equippable_slots.unequip(item) else False

    def calculateItemWorth(self, item: BaseItem) -> int:
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
    print(c.equip(b))
    print(c.inventory.container)
    print(c.unequip(b))
    print(b.slot_type)
    print(c)



if __name__ == '__main__':
    main()