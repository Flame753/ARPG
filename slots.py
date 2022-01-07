from abc import ABC
import items

class Slot(ABC):
    def __init__(self, name=None, item_limit=1):
        self.name = name
        self.item_limit = item_limit

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name}, item_limit={self.item_limit})'

    def ensureInventory(self):
        if not hasattr(self, 'inventory'):
            self.inventory = {}

    def addItem(self, item, amount=0):
        self.ensureInventory()

        if not isinstance(item, items.BaseItem):
            return False
        if len(self.inventory) >= self.item_limit:
            return False
        if item in self.inventory:
            self.inventory[item]['amount'] += amount
            return True
        else:
            self.inventory[item] = {'amount': amount}
            return True
    
    def removeItem(self, item, amount = 0):
        self.ensureInventory()

        if item in self.inventory:
            if self.inventory[item]['amount'] >= amount:
                self.inventory[item]['amount'] -= amount
                if self.inventory[item]['amount'] == 0:
                    del(self.inventory[item])
                return True
        return False

    def calculateItemWeight(self, item):
        self.ensureInventory()
        
        if item in self.inventory:
            return item.weight * self.inventory[item]['amount']

    def calculateItemWorth(self, item):
        self.ensureInventory()
        
        if item in self.inventory:
            return item.worth * self.inventory[item]['amount']

    def calculateTotalWeight(self):
        self.ensureInventory()

        weight = 0
        for item, data in self.inventory.items():
            weight += item.weight * data['amount']
        return weight

    def calculateTotalWorth(self):
        self.ensureInventory()

        worth = 0
        for item, data in self.inventory.items():
            worth += item.worth * data['amount']
        return worth

class Head(Slot):
    def __init__(self):
        super().__init__(name='HeadSlot')

class Body(Slot):
    def __init__(self):
        super().__init__(name='BodySlot')

class Legs(Slot):
    def __init__(self):
        super().__init__(name='LegsSlot')

class OneHand(Slot):
    def __init__(self, name='OneHandSlot'):
        super().__init__(name=name)
    
    def addItem(self, item, amount=0):
        self.ensureInventory()

        if not isinstance(item, items.Weapon):
            return False
        if len(self.inventory) >= self.item_limit:
            return False
        if item in self.inventory:
            self.inventory[item]['amount'] += amount
            return True
        else:
            self.inventory[item] = {'amount': amount}
            return True

class TwoHands(OneHand):
    def __init__(self):
        super().__init__(name='TwoHandsSlot')

class SmallItem(Slot):
    def __init__(self):
        super().__init__(name='SmallItemSlot', item_limit=2)

class Coins(Slot):
    def __init__(self):
        super().__init__(name='CoinSlot', item_limit=10)

    def addItem(self, item, amount=0):
        self.ensureInventory()

        if not isinstance(item, items.Coin):
            return False
        if len(self.inventory) >= self.item_limit:
            return False
        if item in self.inventory:
            self.inventory[item]['amount'] += amount
            return True
        else:
            self.inventory[item] = {'amount': amount}
            return True


if __name__ == "__main__":
    c = Coins()
    print(c.addItem(items.Dagger(), 1))
    print(c.inventory)
    print(c.addItem(items.CopperCoin(), 1))
    print(c.inventory)
    print(c.addItem(items.GraterPlatinumCoin(), 1))
    print(c.inventory)