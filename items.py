from abc import ABC


class BaseItem(ABC):
    def __init__(self, name = None, worth = 0, weight = 0, description = '', **kwargs):
        if type(self) == BaseItem:
            raise Exception('Do not instantiate BaseItem directly')
        self.name = name
        self.worth = worth
        self.weight = weight
        self.description = description

    def modifyAttr(self, **kwargs):
        for key in kwargs.keys():
            if not hasattr(self, key):
                return False

        self.__dict__.update(kwargs)
        return True

    
    def __str__(self):
        if self.description:
            return f'{self.description} {self.name}'
        else:
            return f'{self.name}'

    def __repr__(self):
        return f'{self.__class__.__name__}()'

# Weapons
class Weapon(BaseItem):
    def __init__(self, damage = 0, **kwargs):
        super().__init__(**kwargs)
        self.damage = damage
        if type(self) == Weapon:
            raise Exception('Do not instantiate Weapon directly')

class Rock(Weapon):
    def __init__(self, name='Rock', damage=5, worth=1, weight=1,**kwargs):
        super().__init__(name=name, damage=damage, worth=worth, weight=weight, **kwargs)

class Dagger(Weapon):
    def __init__(self, name='Dagger', damage=10, worth=20, weight=1,**kwargs):
        super().__init__(name=name, damage=damage, worth=worth, weight=weight, **kwargs)

class Sword(Weapon):
    def __init__(self, name='Sword', damage=20, worth=100, weight=1, 
                description='Rusty', **kwargs):
        super().__init__(name=name, damage=damage, worth=worth, weight=weight, 
                        description=description, **kwargs)

class Crossbow(Weapon):
    def __init__(self, name='Crossbow', damage=15, worth=75, weight=2,**kwargs):
        super().__init__(name=name, damage=damage, worth=worth, weight=weight, **kwargs)

class Axe(Weapon):
    def __init__(self, name='Axe', damage=25, worth=60, weight=2,**kwargs):
        super().__init__(name=name, damage=damage, worth=worth, weight=weight, **kwargs)

# Consumables
class Consumable(BaseItem):
    def __init__(self, healing_value = 0, **kwargs):
        super().__init__(**kwargs)
        self.healing_value = healing_value
        if type(self) == Consumable:
            raise Exception('Do not instantiate Consumable directly')

    def __str__(self):
        return f'{self.description} {self.name} (+{self.healing_value})'

class Bread(Consumable):
    def __init__(self, name='Bread', healing_value=10, worth=12, weight=1,
                 description='Crusty', **kwargs):
        super().__init__(name=name, healing_value=healing_value, worth=worth, 
                        weight=weight, description=description **kwargs)


class HealingPotion(Consumable):
    def __init__(self, name="Healing Potion", healing_value=50, worth=60,
                 weight=1, **kwargs):
        super().__init__(name=name, healing_value=healing_value, worth=worth, 
                        weight=weight, **kwargs)

# Containers
class Container(ABC):
    def __init__(self):
        if type(self) == Container:
            raise Exception('Do not instantiate Container directly')

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
    
class Backpack(BaseItem, Container):
    def __init__(self, name='Backpack', worth=10, weight=1,**kwargs):
        super().__init__(name=name, worth=worth, weight=weight, **kwargs)

class CoinPouch(BaseItem, Container):
    def __init__(self, name='Coin Pouch', worth=1, weight=.1, **kwargs):
        super().__init__(name=name, worth=worth, weight=weight, **kwargs)

# Currency
class Coin(BaseItem):
    def __init__(self, **kwargs):
        super().__init__(weight=0.01, **kwargs)
        if type(self) == Coin:
            raise Exception('Do not instantiate Coin directly')

class CopperCoin(Coin):
    def __init__(self, name='Copper Coin', worth=1, **kwargs):
        super().__init__(name=name, worth=worth, **kwargs)

class SilverCoin(Coin):
    def __init__(self, name='Silver Coin', worth=10, **kwargs):
        super().__init__(name=name, worth=worth, **kwargs)


class GoldCoin(Coin):
    def __init__(self, name='Gold Coin', worth=100, **kwargs):
        super().__init__(name=name, worth=worth, **kwargs)

class PlatinumCoin(Coin):
    def __init__(self, name='Platinum Coin', worth=1000, **kwargs):
        super().__init__(name=name, worth=worth, **kwargs)
        

if __name__ == "__main__":
    # BaseItem()
    # Weapon()
    # Consumable()
    # Container()
    # Coin()
    print([CopperCoin(), Bread(), Sword()])
    print(CopperCoin(), Dagger(), Bread(), Backpack(), Sword())
    
    c = CopperCoin()
    print(c.modifyAttr(name="l", ru=1))
    print(c.modifyAttr(name="small copper coin"))
    print(c.__dict__)

    backpack = Backpack()
    backpack.addItem(CopperCoin(), 10)
    print('Backpack: worth -> {}, weight -> {}'.format(backpack.calculateTotalWorth(), backpack.calculateTotalWeight()))
    backpack.addItem(GoldCoin(), 53)
    print('Backpack: worth -> {}, weight -> {}'.format(backpack.calculateTotalWorth(), backpack.calculateTotalWeight()))

