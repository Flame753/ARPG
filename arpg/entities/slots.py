# Standard library imports 
from __future__ import annotations  # Allowing commodity.items for typehinting and preventing cycle ImportError
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pprint import pprint

# Local application imports
import entities.items as items



class CapacityReachedError(Exception):
    """Exception raised for reaching the capacity."""
    
    def __init__(self, message="Item was attempted to be added, but capacity already reached!"):
        self.message = message
        super().__init__(self.message)



@dataclass
class Container(ABC):
    container: dict = field(default_factory=dict, init=False)
    
    @abstractmethod
    def add_item(self, item, amount=0):
        pass

    @abstractmethod
    def remove_item(self, item, amount = 0):
        pass

    @abstractmethod
    def calculate_item_weight(self, item):
        pass

    @abstractmethod
    def calculate_item_worth(self, item):
        pass

    @abstractmethod
    def calculate_total_weight(self):
        pass

    @abstractmethod
    def calculate_total_worth(self):
        pass

@dataclass()
class Slot(Container):
    name: str = None
    item_limit: int = None
    
    def add_item(self, item: items.BaseItem, amount: int=1) -> bool:
        if self._is_capacity_reached(amount):
            raise CapacityReachedError(f"Exceeded Maximum Capacity of {self.item_limit}! Unable to add {item}!")
        if item in self.container:
            self.container[item]['amount'] += amount # Adding another item
        else:
            self.container[item] = {'amount': amount} # Adding new item

    def _is_capacity_reached(self, additional_amount: int=0) -> bool:
        if self.item_limit == None: return False
        amount_list = [amount['amount'] for amount in self.container.values()]
        total_amount = sum(amount_list) + additional_amount
        if total_amount == 0 and self.item_limit == 0: return True
        return total_amount > self.item_limit

    def remove_item(self, item: items.BaseItem, amount: int=1) -> bool:
        if item in self.container:
            if self.container[item]['amount'] >= amount:
                self.container[item]['amount'] -= amount
                if self.container[item]['amount'] == 0:
                    del(self.container[item])
                return True
        return False

    def calculate_item_weight(self, item: items.BaseItem) -> int:
        raise NotImplementedError()
        total_amount_weight = item.weight * self.container[item]['amount']
        return total_amount_weight if item in self.container else 0

    def calculate_item_worth(self, item: items.BaseItem) -> int:
        total_amount_worth = item.worth * self.container[item]['amount']
        return total_amount_worth if item in self.container else 0

    def calculate_total_weight(self) -> int:
        raise NotImplementedError()
        weight = 0
        for item, data in self.container.items():
            weight += item.weight * data['amount']
        return weight

    def calculate_total_worth(self) -> int:
        worth = 0
        for item, data in self.container.items():
            worth += item.worth * data['amount']
        return worth

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
        currently_own = self.container.get(coin, 0)
        if type(currently_own) == dict:
            currently_own = currently_own['amount']
        return currently_own >= amount

    def order(self, reverse:bool=False) -> None:
        # rearrange the container from smallest to largest worth
        coins = list(self.container.items())
        worth = lambda coin: coin[0].worth
        coins.sort(key=worth, reverse=reverse)  # Sort function only works with a list name
        ordict = dict(coins)
        self.container.clear()
        self.container.update(ordict)

    def find_largest_coin(self) -> items.Coin:
        self.order()
        coins = list(self.container.items())
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
        if not self.locate_slot_by_item(item): return False
        return True if item in self.locate_slot_by_item(item).container else False

    def locate_slot_by_item(self, item: items.BaseItem) -> Slot:
        return self.slots.get(item.slot_type)
