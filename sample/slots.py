from abc import ABC, abstractmethod
from audioop import add
from dataclasses import dataclass, field
# from container import Container
from items import BaseItem
import setting



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
    type: str = None
    item_limit: int = None
    
    def addItem(self, item: BaseItem, amount: int=1) -> bool:
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

    def _isCorrectSlot(self, item: BaseItem) -> bool:
        pass

    def removeItem(self, item, amount=1):
        if item in self.container:
            if self.container[item]['amount'] >= amount:
                self.container[item]['amount'] -= amount
                if self.container[item]['amount'] == 0:
                    del(self.container[item])
                return True
        return False

    def calculateItemWeight(self, item):
        raise NotImplementedError()
        total_amount_weight = item.weight * self.container[item]['amount']
        return total_amount_weight if item in self.container else 0

    def calculateItemWorth(self, item):
        total_amount_worth = item.worth * self.container[item]['amount']
        return total_amount_worth if item in self.container else 0

    def calculateTotalWeight(self):
        raise NotImplementedError()
        weight = 0
        for item, data in self.container.items():
            weight += item.weight * data['amount']
        return weight

    def calculateTotalWorth(self):
        worth = 0
        for item, data in self.container.items():
            worth += item.worth * data['amount']
        return worth

@dataclass()
class Head(Slot):
    type: str = setting.HEAD_SLOT
    item_limit: int = 1

@dataclass()
class Body(Slot):
    type: str = setting.BODY_SLOT
    item_limit: int = 1

@dataclass()
class Legs(Slot):
    type: str = setting.LEGS_SLOT
    item_limit: int = 1

@dataclass()
class Boots(Slot):
    type: str = setting.BOOTS_SLOT
    item_limit: int = 1

@dataclass()
class OneHanded(Slot):
    type: str = setting.ONE_HANDED_SLOT
    item_limit: int = 1
    
@dataclass()    
class TwoHanded(Slot):
    type: str = setting.TWO_HANDED_SLOT
    item_limit: int = 1

@dataclass()
class Coins(Slot):
    type: str = setting.COIN_SLOT

    def order(self) -> list:
        # Puts the container from largest worth to smallest
        coins = list(self.container.items())
        worth = lambda coin: coin[0].worth
        coins.sort(key=worth)  # Sort function only works with a list type
        ordict = dict(coins)
        self.container.clear()
        self.container.update(ordict)

@dataclass()
class Miscellaneous(Slot):
    type: str = setting.MISC_SLOT


class EquipmentSlots():
    def __init__(self):
        self.slots = {setting.HEAD_SLOT: Head(),
                        setting.BODY_SLOT: Body(),
                        setting.LEGS_SLOT: Legs(),
                        setting.BOOTS_SLOT: Boots(),
                        setting.ONE_HANDED_SLOT: OneHanded(),
                        setting.TWO_HANDED_SLOT: TwoHanded()}

    def equip(self, item: BaseItem) -> bool:
        if not self.locateSlotByItem(item): return
        self.locateSlotByItem(item).addItem(item, 1)

        # try:
        #     # Adds item and checks if item was added
        #     self.locateSlotByItem(item).addItem(item, 1)
        #     return True
        # except CapacityReachedError:
        #     # Capacity was reached
        #     return False

    def unequip(self, item: BaseItem) -> bool:
        if not self.isItemEquipped(item): return False
        return True if self.locateSlotByItem(item).removeItem(item, 1) else False

    def isItemEquipped(self, item: BaseItem) -> bool:
        if not self.locateSlotByItem(item): return False
        return True if item in self.locateSlotByItem(item).container else False

    def locateSlotByItem(self, item: BaseItem) -> Slot:
        return self.slots.get(item.slot_type)



def main():
    import items
    a = OneHanded()
    b = OneHanded()
    c = TwoHanded()
    a1 = items.Bread()
    a.addItem(a1, 2)




if __name__ == "__main__":
    main()
