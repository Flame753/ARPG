from abc import ABC
from dataclasses import dataclass, field
import setting


@dataclass()
class Slot(ABC):
    name: str = None
    inventory: list = field(default_factory=list)

    def addItem(self, item, amount=0):
        if item in self.inventory:
            self.inventory[item]['amount'] += amount
        else:
            self.inventory[item] = {'amount': amount}
    
    def removeItem(self, item, amount = 0):
        if item in self.inventory:
            if self.inventory[item]['amount'] >= amount:
                self.inventory[item]['amount'] -= amount
                if self.inventory[item]['amount'] == 0:
                    del(self.inventory[item])
                return True
        return False

    def amountOfItems(self):
        total_amount = 0
        for data in self.inventory.values():
            total_amount += data['amount']
        return total_amount

    def calculateItemWeight(self, item):
        if item in self.inventory:
            return item.weight * self.inventory[item]['amount']

    def calculateItemWorth(self, item):
        if item in self.inventory:
            return item.worth * self.inventory[item]['amount']

    def calculateTotalWeight(self):
        weight = 0
        for item, data in self.inventory.items():
            weight += item.weight * data['amount']
        return weight

    def calculateTotalWorth(self):
        worth = 0
        for item, data in self.inventory.items():
            worth += item.worth * data['amount']
        return worth

@dataclass()
class Head(Slot):
    name: str = setting.HEAD_SLOT

@dataclass()
class Body(Slot):
    name: str = setting.BODY_SLOT

@dataclass()
class Legs(Slot):
    name: str = setting.LEGS_SLOT

@dataclass()
class OneHanded(Slot):
    name: str = setting.TWO_HANDED_SLOT
    
@dataclass()    
class TwoHanded(Slot):
    name: str = setting.ONE_HANDED_SLOT

@dataclass()
class Coins(Slot):
    name: str = setting.COIN_SLOT

    def order(self) -> list:
        # Puts the inventory from largest worth to smallest
        coins = list(self.inventory.items())
        worth = lambda coin: coin[0].worth
        coins.sort(key=worth)  # Sort function only works with a list type
        ordict = dict(coins)
        self.inventory.clear()
        self.inventory.update(ordict)

@dataclass()
class Miscellaneous(Slot):
    name: str = setting.MISC_SLOT


def main():
    import items
    s = Slot()
    print(s.inventory)

if __name__ == "__main__":
    main()
