# Standard library imports 
from dataclasses import dataclass, field
from pprint import pprint

# Local application imports
from entities.items import BaseItem
from entities import slots



class EquippedItemRemovealError(Exception):
    """Exception raised for not unequipped existing item before removing the item."""
    
    def __init__(self, message="Item was attempted to be removed, before being unequipped!"):
        self.message = message
        super().__init__(self.message)


# @dataclass() 
class Creature():
    def __init__(self):
        self.inventory = slots.Miscellaneous()
        self.coin_pouch = slots.Coins()
        self.equippable_slots = slots.EquipmentSlots()
        self.hp = 100
        self.max_hp = 100


    def _verify_arguments(self, item: BaseItem=None, amount: int=None) -> None:
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

    def add_item(self, item: BaseItem, amount: int=1) -> None:
        self._verify_arguments(item, amount)

        # Always adds the amount of items into the invenotry slot excluding any Coin items
        if item.slot_type == slots.Coins:
            self.coin_pouch.add_item(item, amount)
        else:
            self.inventory.add_item(item, amount)

    def remove_item(self, item: BaseItem, amount: int=1) -> bool:
        self._verify_arguments(item, amount)

        if self.equippable_slots.is_item_equipped(item): raise EquippedItemRemovealError

        if item.slot_type == slots.Coins:
            return self.coin_pouch.remove_item(item, amount)
        else:
            return self.inventory.remove_item(item, amount)

    def equip(self, item: BaseItem) -> bool:
        self._verify_arguments(item)

        if not item in self.inventory.container: return False # No items to equip
        return self.equippable_slots.equip(item)

    def unequip(self, item: BaseItem) -> bool:
        self._verify_arguments(item)

        return True if self.equippable_slots.unequip(item) else False

    def calculate_item_worth(self, item: BaseItem) -> int:
        self._verify_arguments(item)

        if item.slot_type == slots.Coins:
            return self.coin_pouch.calculate_item_worth(item)
        else:
            return self.inventory.calculate_item_worth(item)

    def calculate_total_worth(self) -> int:
        return self.coin_pouch.calculate_total_worth() + self.inventory.calculate_total_worth()

    def is_alive(self) -> bool:
        return self.hp > 0
