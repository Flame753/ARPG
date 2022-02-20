from abc import ABC, abstractmethod
from dataclasses import dataclass, field
# from container import Container
from items import BaseItem
import setting



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
    
    def addItem(self, item: BaseItem, amount: int=0) -> bool:
        # Checks if there a limit or not
        if self.item_limit:
            # Check if limit was passed
            if len(self.container) >= self.item_limit: 
                raise IndexError(f"Exceeded Maximum Capacity of {self.item_limit}! Unable to add {item}!")
        # Adds another items if exist
        if item in self.container:
            self.container[item]['amount'] += amount
        # Adds new item
        else:
            self.container[item] = {'amount': amount}
    
    def removeItem(self, item, amount = 0):
        if item in self.container:
            if self.container[item]['amount'] >= amount:
                self.container[item]['amount'] -= amount
                if self.container[item]['amount'] == 0:
                    del(self.container[item])
                return True
        return False

    def calculateItemWeight(self, item):
        raise NotImplementedError()
        if item in self.container:
            return item.weight * self.container[item]['amount']
        return 0

    def calculateItemWorth(self, item):
        if item in self.container:
            return item.worth * self.container[item]['amount']
        return 0

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



def main():
    import items
    a = OneHanded()
    b = OneHanded()
    c = TwoHanded()
    a1 = items.Bread()
    a.addItem(a1, 2)




if __name__ == "__main__":
    main()
