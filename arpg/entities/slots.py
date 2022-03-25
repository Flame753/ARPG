# Standard library imports 
from dataclasses import dataclass
from typing import Optional
from pprint import pprint

# Local application imports
from entities.utils import Container
from entities import items
from entities import currency



class CapacityReachedError(Exception):
    """Exception raised for reaching the capacity."""
    
    def __init__(self, message="Item was attempted to be added, but capacity already reached!"):
        self.message = message
        super().__init__(self.message)

class ItemFilterError(Exception):
    """Exception raised for invaild item type."""
    
    def __init__(self, message="Invaild item type for this Slot!"):
        self.message = message
        super().__init__(self.message)



@dataclass()
class Slot(Container):
    def __init__(self, name, items_type):
        self.name: str = name
        self.items_allowed: items.BaseItem = items_type
    
    def add_item(self, item, amount: int=1) -> bool:
        if not isinstance(item, self.items_allowed):
            raise ItemFilterError(f"An Invaild Item '{item}' for the {self.name}! ")
        super().add_item(item, amount)

    def remove_item(self, item, amount: int=1) -> bool:
        return super().remove_item(item, amount)

    def total_amount_of_item(self) -> int:
        return sum([amount['amount'] for amount in self.inventory.values()])

@dataclass()
class Coins(Slot):
    name: str = "Coin Slot"
    items_allowed: currency.Coin = currency.Coin

    def have_coin(self, coin, amount=1):
        self._ensure_inventory()
        if amount <= 0: raise ValueError 

        currently_own = self.inventory.get(coin, 0)
        if type(currently_own) == dict:
            currently_own = currently_own['amount']
        return currently_own >= amount

    def order(self, reverse:bool=False) -> list[currency.Coin]:
        # rearrange the inventory from smallest to largest worth
        self._ensure_inventory()
        coins = list(self.inventory.keys())
        worth = lambda coin: coin.worth
        coins.sort(key=worth, reverse=reverse)  # Sort function only works with a list name
        return coins

    def find_largest_coin(self) -> Optional[currency.Coin]:
        coins = self.order()
        return coins.pop() if coins else None 

@dataclass
class Items(Slot):
    name: str = "Item Slot"
    items_allowed: items.BaseItem = items.BaseItem

@dataclass
class Consumables(Slot):
    name: str = "Consumable Slot"
    items_allowed: items.Consumable = items.Consumable

@dataclass
class Weapons(Slot):
    name: str = "Weapon Slot"
    items_allowed: items.Weapon = items.Weapon

@dataclass
class Armor(Slot):
    name: str = "Armor Slot"
    items_allowed: items.Armor = items.Armor


@dataclass()
class EquippableSlots(Slot):
    def __init__(self, name, items_type, item_limit):
        super().__init__(name, items_type)
        self.item_limit: int = item_limit

    def _capacity_reached(self) -> bool:
        self._ensure_inventory()
        total_amount = self.total_amount_of_item()
        if total_amount == 0 and self.item_limit == 0: return True
        return total_amount >= self.item_limit

    def add_item(self, item, amount: int=1) -> bool:
        if not isinstance(item, self.items_allowed):
            raise ItemFilterError(f"An Invaild Item '{item}' for the {self.name}! ")
        if self._capacity_reached() or (self.total_amount_of_item() + amount) > self.item_limit:
            raise CapacityReachedError(f"Exceeded Maximum Capacity of {self.item_limit}! Unable to add {item}!")
        Container.add_item(self, item, amount)

@dataclass()
class Head(EquippableSlots):
    name: str = "Head Slot"
    item_limit: int = 1
    items_allowed: items.Helmet = items.Helmet

@dataclass()
class Body(EquippableSlots):
    name: str = "Body Slot"
    item_limit: int = 1
    items_allowed: items.Chest = items.Chest

@dataclass()
class Legs(EquippableSlots):
    name: str = "Legs Slot"
    item_limit: int = 1
    items_allowed: items.Pants = items.Pants

@dataclass()
class Boots(EquippableSlots):
    name: str = "Boots Slot"
    item_limit: int = 1
    items_allowed: items.Boots = items.Boots

@dataclass()
class OneHanded(EquippableSlots):
    name: str = "One Handed Slot"
    item_limit: int = 1
    items_allowed: items.OneHandedWeapon = items.OneHandedWeapon
    
@dataclass()    
class TwoHanded(EquippableSlots):
    name: str = "Two Handed Slot"
    item_limit: int = 1
    items_allowed: items.TwoHandedWeapon = items.TwoHandedWeapon

