from abc import ABC, abstractmethod
from dataclasses import dataclass, field
# from container import Container
from items import BaseItem
import setting



@dataclass
class Container(ABC):
    items: dict = field(default_factory=dict, init=False)
    
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
    
    def addItem(self, item: BaseItem, amount: int=0) -> bool:
        # Checks if there a limit or not
        if self.item_limit:
            # Check if limit was passed
            if len(self.items) >= self.item_limit: 
                raise IndexError(f"Exceeded Maximum Capacity of {self.item_limit}! Unable to add {item}!")
        # Adds another items if exist
        if item in self.items:
            self.items[item]['amount'] += amount
        # Adds new item
        else:
            self.items[item] = {'amount': amount}
    
    def removeItem(self, item, amount = 0):
        if item in self.items:
            if self.items[item]['amount'] >= amount:
                self.items[item]['amount'] -= amount
                if self.items[item]['amount'] == 0:
                    del(self.items[item])
                return True
        return False

    def calculateItemWeight(self, item):
        raise NotImplementedError()
        if item in self.items:
            return item.weight * self.items[item]['amount']
        return 0

    def calculateItemWorth(self, item):
        if item in self.items:
            return item.worth * self.items[item]['amount']
        return 0

    def calculateTotalWeight(self):
        raise NotImplementedError()
        weight = 0
        for item, data in self.items.items():
            weight += item.weight * data['amount']
        return weight

    def calculateTotalWorth(self):
        worth = 0
        for item, data in self.items.items():
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

@dataclass()
class Miscellaneous(Slot):
    type: str = setting.MISC_SLOT



def main():
    import items
    a = OneHanded()
    b = OneHanded()
    c = TwoHanded()
    a1 = items.Bread()
    a.addItem(a1, 2)

    # i = Inventory()
    # print('test', i.isEmpty())
    # i.addItem(items.Dagger())
    # print('test', i.isEmpty())



if __name__ == "__main__":
    main()
