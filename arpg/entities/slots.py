# Standard library imports 
from __future__ import annotations  # Allowing commodity.items for typehinting and preventing cycle ImportError
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from pprint import pprint

# Local application imports
import entities.items as items



class CapacityReachedError(Exception):
    """Exception raised for reaching the capacity."""
    
    def __init__(self, message="Item was attempted to be added, but capacity already reached!"):
        self.message = message
        super().__init__(self.message)



class Container(ABC):
    def _ensure_inventory(self) -> None:
        if not hasattr(self, 'inventory'):
            self.inventory = dict()

    def add_item(self, item: items.BaseItem, amount: int = 0) -> None:
        self._ensure_inventory()

        if item in self.inventory:
            self.inventory[item]['amount'] += amount
        else:
            self.inventory[item] = {'amount': amount}

    def remove_item(self, item: items.BaseItem, amount: int = 0) -> bool:
        self._ensure_inventory()

        if item in self.inventory:
            if self.inventory[item]['amount'] >= amount:
                self.inventory[item]['amount'] -= amount
                if self.inventory[item]['amount'] == 0:
                    del(self.inventory[item])
                return True
        return False

    def calculate_item_weight(self, item: items.BaseItem) -> int:
        self._ensure_inventory()

        if item in self.inventory:
            return item.weight * self.inventory[item]['amount']

    def calculate_item_worth(self, item: items.BaseItem)  -> int:
        self._ensure_inventory()

        if item in self.inventory:
            return item.worth * self.inventory[item]['amount']

    def calculate_total_weight(self) -> int:
        self._ensure_inventory()

        weight = 0
        for item, data in self.inventory.items():
            weight += item.weight * data['amount']
        return weight

    def calculate_total_worth(self) -> int:
        self._ensure_inventory()

        worth = 0
        for item, data in self.inventory.items():
            worth += item.worth * data['amount']
        return worth


@dataclass()
class Slot(Container):
    def __init__(self, name, item_limit):
        self.name: str = name
        self.item_limit: int = item_limit
    
    def add_item(self, item: items.BaseItem, amount: int=1) -> bool:
        if self._is_capacity_reached(amount):
            raise CapacityReachedError(f"Exceeded Maximum Capacity of {self.item_limit}! Unable to add {item}!")
        super().add_item(item, amount)

    def _is_capacity_reached(self, additional_amount: int=0) -> bool:
        if not hasattr(self, 'item_limit'): return False
        self._ensure_inventory()
        amount_list = [amount['amount'] for amount in self.inventory.values()]
        total_amount = sum(amount_list) + additional_amount
        if total_amount == 0 and self.item_limit == 0: return True
        return total_amount > self.item_limit

    def remove_item(self, item: items.BaseItem, amount: int=1) -> bool:
        return super().remove_item(item, amount)

    def calculate_item_worth(self, item: items.BaseItem) -> int:
        self._ensure_inventory()
        total_amount_worth = item.worth * self.inventory[item]['amount']
        return total_amount_worth if item in self.inventory else 0


@dataclass()
class Head(Slot):
    name: str = "Head Slot"
    item_limit: int = 1

@dataclass()
class Body(Slot):
    name: str = "Body Slot"
    item_limit: int = 1

@dataclass()
class Legs(Slot):
    name: str = "Legs Slot"
    item_limit: int = 1

@dataclass()
class Boots(Slot):
    name: str = "Boots Slot"
    item_limit: int = 1

@dataclass()
class OneHanded(Slot):
    name: str = "One Handed Slot"
    item_limit: int = 1
    
@dataclass()    
class TwoHanded(Slot):
    name: str = "Two Handed Slot"
    item_limit: int = 1

@dataclass()
class Coins(Slot):
    name: str = "Coin Slot"

    def have_coin(self, coin, amount=1):
        self._ensure_inventory()
        if amount <= 0: raise ValueError 

        currently_own = self.inventory.get(coin, 0)
        if type(currently_own) == dict:
            currently_own = currently_own['amount']
        return currently_own >= amount

    def order(self, reverse:bool=False) -> None:
        # rearrange the inventory from smallest to largest worth
        self._ensure_inventory()
        coins = list(self.inventory.items())
        worth = lambda coin: coin[0].worth
        coins.sort(key=worth, reverse=reverse)  # Sort function only works with a list name
        ordict = dict(coins)
        self.inventory.clear()
        self.inventory.update(ordict)

    def find_largest_coin(self) -> items.Coin:
        self.order()
        coins = list(self.inventory.items())
        return coins[-1][0]


@dataclass()
class Miscellaneous(Slot):
    name: str = "Miscellaneous Slot"

class EquipmentSlots():
    def __init__(self):
        self.slots = {Head: Head(),
                        Body: Body(),
                        Legs: Legs(),
                        Boots: Boots(),
                        OneHanded: OneHanded(),
                        TwoHanded: TwoHanded()}

    def equip(self, item: items.BaseItem) -> bool:
        if not self.locate_slot_by_item(item): return False
        self.locate_slot_by_item(item).add_item(item, 1)
        return True

    def unequip(self, item: items.BaseItem) -> bool:
        if not self.is_item_equipped(item): return False
        return True if self.locate_slot_by_item(item).remove_item(item, 1) else False

    def is_item_equipped(self, item: items.BaseItem) -> bool:
        slot = self.locate_slot_by_item(item)
        if not slot: return False
        slot._ensure_inventory()
        return True if item in slot.inventory else False

    def locate_slot_by_item(self, item: items.BaseItem) -> Optional[Slot]:
        return self.slots.get(item.slot_type)
