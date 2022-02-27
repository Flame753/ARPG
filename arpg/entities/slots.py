# Standard library imports 
from __future__ import annotations  # Allowing items.BaseItem for typehinting and preventing cycle ImportError
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
    def addItem(self, item, amount=0):
        pass

    @abstractmethod
    def removeItem(self, item, amount = 0):
        pass

    @abstractmethod
    def calculateItemWeight(self, item):
        pass

    @abstractmethod
    def calculateItemWorth(self, item):
        pass

    @abstractmethod
    def calculateTotalWeight(self):
        pass

    @abstractmethod
    def calculateTotalWorth(self):
        pass

@dataclass()
class Slot(Container):
    name: str = None
    item_limit: int = None
    
    def addItem(self, item: items.BaseItem, amount: int=1) -> bool:
        if self._isCapacityReached(amount):
            raise CapacityReachedError(f"Exceeded Maximum Capacity of {self.item_limit}! Unable to add {item}!")
        if item in self.container:
            self.container[item]['amount'] += amount # Adding another item
        else:
            self.container[item] = {'amount': amount} # Adding new item

    def _isCapacityReached(self, additional_amount: int=0) -> bool:
        if self.item_limit == None: return False
        amount_list = [amount['amount'] for amount in self.container.values()]
        total_amount = sum(amount_list) + additional_amount
        if total_amount == 0 and self.item_limit == 0: return True
        return total_amount > self.item_limit

    def removeItem(self, item: items.BaseItem, amount: int=1) -> bool:
        if item in self.container:
            if self.container[item]['amount'] >= amount:
                self.container[item]['amount'] -= amount
                if self.container[item]['amount'] == 0:
                    del(self.container[item])
                return True
        return False

    def calculateItemWeight(self, item: items.BaseItem) -> int:
        raise NotImplementedError()
        total_amount_weight = item.weight * self.container[item]['amount']
        return total_amount_weight if item in self.container else 0

    def calculateItemWorth(self, item: items.BaseItem) -> int:
        total_amount_worth = item.worth * self.container[item]['amount']
        return total_amount_worth if item in self.container else 0

    def calculateTotalWeight(self) -> int:
        raise NotImplementedError()
        weight = 0
        for item, data in self.container.items():
            weight += item.weight * data['amount']
        return weight

    def calculateTotalWorth(self) -> int:
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

    def order(self) -> list:
        # Puts the container from largest worth to smallest
        coins = list(self.container.items())
        worth = lambda coin: coin[0].worth
        coins.sort(key=worth)  # Sort function only works with a list name
        ordict = dict(coins)
        self.container.clear()
        self.container.update(ordict)

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
        if not self.locateSlotByItem(item): return False
        self.locateSlotByItem(item).addItem(item, 1)
        return True

    def unequip(self, item: items.BaseItem) -> bool:
        if not self.isItemEquipped(item): return False
        return True if self.locateSlotByItem(item).removeItem(item, 1) else False

    def isItemEquipped(self, item: items.BaseItem) -> bool:
        if not self.locateSlotByItem(item): return False
        return True if item in self.locateSlotByItem(item).container else False

    def locateSlotByItem(self, item: items.BaseItem) -> Slot:
        return self.slots.get(item.slot_type)
