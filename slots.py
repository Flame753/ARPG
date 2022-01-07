from abc import ABC


class Slot(ABC):
    def __init__(self, name=None, item_limit=1, **kwargs):
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
        # if not isinstance(item, self.valid_type):
        #     return False
        if len(self.inventory) + amount > self.item_limit:
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
    def __init__(self, **kwargs):
        super().__init__(name='HeadSlot', **kwargs)

class Body(Slot):
    def __init__(self, **kwargs):
        super().__init__(name='BodySlot', **kwargs)

class Legs(Slot):
    def __init__(self, **kwargs):
        super().__init__(name='LegsSlot', **kwargs)

class OneHand(Slot):
    def __init__(self, name='OneHandSlot', item_limit=2, **kwargs):
        super().__init__(name=name, item_limit=item_limit, **kwargs)
    
class TwoHands(OneHand):
    def __init__(self, **kwargs):
        super().__init__(name='TwoHandsSlot', **kwargs)

class SmallItem(Slot):
    def __init__(self, **kwargs):
        super().__init__(name='SmallItemSlot', item_limit=2, **kwargs)

class Coins(Slot):
    def __init__(self, **kwargs):
        super().__init__(name='CoinSlot', item_limit=10, **kwargs)


if __name__ == "__main__":
    import items
    c = Coins()
    print(c.addItem(items.Dagger(), 1))
    print(c.inventory)
    print(c.addItem(items.CopperCoin(), 1))
    print(c.inventory)
    print(c.addItem(items.GraterPlatinumCoin(), 1))
    print(c.inventory)