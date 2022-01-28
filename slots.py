from abc import ABC


class Slot(ABC):
    def __init__(self, name=None, **kwargs):
        self.name = name

    def __str__(self):
        return f'{self.name} Slot'

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name})'

    def ensureInventory(self):
        if not hasattr(self, 'inventory'):
            self.inventory = {}

    def addItem(self, item, amount=0):
        self.ensureInventory()
        if item in self.inventory:
            self.inventory[item]['amount'] += amount
        else:
            self.inventory[item] = {'amount': amount}
    
    def removeItem(self, item, amount = 0):
        self.ensureInventory()

        if item in self.inventory:
            if self.inventory[item]['amount'] >= amount:
                self.inventory[item]['amount'] -= amount
                if self.inventory[item]['amount'] == 0:
                    del(self.inventory[item])
                return True
        return False

    def amountOfItems(self):
        self.ensureInventory()

        total_amount = 0
        for data in self.inventory.values():
            total_amount += data['amount']
        return total_amount

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
        super().__init__(name='Head', **kwargs)

class Body(Slot):
    def __init__(self, **kwargs):
        super().__init__(name='Body', **kwargs)

class Legs(Slot):
    def __init__(self, **kwargs):
        super().__init__(name='Legs', **kwargs)

class OneHand(Slot):
    def __init__(self, name='One Hand', **kwargs):
        super().__init__(name=name, **kwargs)
    
class TwoHands(OneHand):
    def __init__(self, **kwargs):
        super().__init__(name='Two Hands', **kwargs)

class SmallItem(Slot):
    def __init__(self, **kwargs):
        super().__init__(name='Small Item', **kwargs)

class Coins(Slot):
    def __init__(self, **kwargs):
        super().__init__(name='Coin', **kwargs)

    def order(self) -> list:
        # Puts the inventory from largest worth to smallest
        coins = list(self.inventory.items())
        worth = lambda coin: coin[0].worth
        coins.sort(key=worth)  # Sort function only works with a list type
        ordict = dict(coins)
        self.inventory.clear()
        self.inventory.update(ordict)

class Miscellaneous(Slot):
    def __init__(self, **kwargs):
        super().__init__(name='Miscellaneous', **kwargs)

def main():
    import items
    c = Coins()
    # print(c.addItem(items.Dagger(), 1))
    # print(c.inventory)
    # print(c.addItem(items.CopperCoin(), 1))
    # print(c.inventory)
    # print(c.addItem(items.GraterPlatinumCoin(), 1))
    # print(c.inventory)
    # print(c.amountOfItems())
    # c.addItem(items.Dagger(), 5)
    # print(c.amountOfItems())
    c.addItem(items.SilverCoin(), 3)

    c.addItem(items.CopperCoin(), 4)
    # c.addItem(items.Backpack)
    c.order()
    # print(c.inventory)

if __name__ == "__main__":
    main()
