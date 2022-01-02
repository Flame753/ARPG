from abc import ABC, abstractstaticmethod


class BaseItem(ABC):
    def __init__(self, name = None, worth = 0, weight = 0, description = '', **kwargs):
        if type(self) == BaseItem:
            raise Exception('Do not instantiate BaseItem directly')
        self.name = name
        self.worth = worth
        self.weight = weight
        self.description = description

    def modify_attr(self, **kwargs):
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
                        weight=weight, description=description, **kwargs)

class HealingPotion(Consumable):
    def __init__(self, name="Healing Potion", healing_value=50, worth=60,
                 weight=1, **kwargs):
        super().__init__(name=name, healing_value=healing_value, worth=worth, 
                        weight=weight, **kwargs)

# Containers
class Inventory(ABC):

    def ensure_inventory(self):
        if not hasattr(self, 'inventory'):
            self.inventory = {}
    
    @abstractstaticmethod
    def add_item():
        pass

    @abstractstaticmethod
    def remove_item():
        pass

    @abstractstaticmethod
    def calculate_total_weight():
        pass

    @abstractstaticmethod
    def calculate_total_worth():
        pass

class Container(Inventory):
    def __init__(self, **kwargs):
        if type(self) == Container:
            raise Exception('Do not instantiate Container directly')
        super().__init__(**kwargs)
    
    def add_item(self, item, amount=0):
        self.ensure_inventory()

        if item in self.inventory:
            self.inventory[item]['amount'] += amount
        else:
            self.inventory[item] = {'amount': amount}
    
    def remove_item(self, item, amount = 0):
        self.ensure_inventory()

        if item in self.inventory:
            if self.inventory[item]['amount'] >= amount:
                self.inventory[item]['amount'] -= amount
                if self.inventory[item]['amount'] == 0:
                    del(self.inventory[item])
                return True
        return False

    def calculate_item_weight(self, item):
        self.ensure_inventory()
        
        if item in self.inventory:
            return item.weight * self.inventory[item]['amount']

    def calculate_item_worth(self, item):
        self.ensure_inventory()
        
        if item in self.inventory:
            return item.worth * self.inventory[item]['amount']

    def calculate_total_weight(self):
        self.ensure_inventory()

        weight = 0
        for item, data in self.inventory.items():
            weight += item.weight * data['amount']
        return weight

    def calculate_total_worth(self):
        self.ensure_inventory()

        worth = 0
        for item, data in self.inventory.items():
            worth += item.worth * data['amount']
        return worth
    
class Backpack(Container, BaseItem):
    def __init__(self, name='Backpack', worth=10, weight=1,**kwargs):
        super().__init__(name=name, worth=worth, weight=weight, **kwargs)

class CoinPouch(Container, BaseItem):
    def __init__(self, name='Coin Pouch', worth=1, weight=.1, **kwargs):
        super().__init__(name=name, worth=worth, weight=weight, **kwargs)

# Currency
class Coin(BaseItem):
    def __init__(self, worth=1, purity=1, **kwargs):
        super().__init__(weight=0.01, **kwargs)
        self.purity = purity
        self.worth = worth * purity
        if type(self) == Coin:
            raise Exception('Do not instantiate Coin directly')

class GreaterCoin(Coin):
    def __init__(self, **kwargs):
        super().__init__(purity=5, **kwargs)
        if type(self) == Coin:
            raise Exception('Do not instantiate GreaterCoin directly')

class CopperCoin(Coin):
    def __init__(self, name='Copper Coin', worth=1, **kwargs):
        super().__init__(name=name, worth=worth, **kwargs)

class GreaterCopperCoin(GreaterCoin, CopperCoin):
    def __init__(self, name='Greater Copper Coin', **kwargs):
        super().__init__(name=name, **kwargs)

class SilverCoin(Coin):
    def __init__(self, name='Silver Coin', worth=10, **kwargs):
        super().__init__(name=name, worth=worth, **kwargs)

class GreaterSilverCoin(GreaterCoin, SilverCoin):
    def __init__(self, name='Greater Silver Coin', **kwargs):
        super().__init__(name=name, **kwargs)

class GoldCoin(Coin):
    def __init__(self, name='Gold Coin', worth=100, **kwargs):
        super().__init__(name=name, worth=worth, **kwargs)

class GreaterGoldCoin(GreaterCoin, SilverCoin):
    def __init__(self, name='Greater Gold Coin', **kwargs):
        super().__init__(name=name, **kwargs)

class PlatinumCoin(Coin):
    def __init__(self, name='Platinum Coin', worth=1000, **kwargs):
        super().__init__(name=name, worth=worth, **kwargs)

class GraterPlatinumCoin(GreaterCoin, PlatinumCoin):
    def __init__(self, name='Greater Platinum Coin', **kwargs):
        super().__init__(name=name, **kwargs)


if __name__ == "__main__":
    # BaseItem()
    # Weapon()
    # Consumable()
    # Container()
    # Coin()
    print([CopperCoin(), Bread(), Sword()])
    print(CopperCoin(), Dagger(), Bread(), Backpack(), Sword())
    
    c = CopperCoin()
    print(c.modify_attr(name="l", ru=1))
    print(c.modify_attr(name="small copper coin"))
    print(c.__dict__)

    backpack = Backpack()
    backpack.add_item(CopperCoin(), 10)
    print('Backpack: worth -> {}, weight -> {}'.format(backpack.calculate_total_worth(), backpack.calculate_total_weight()))
    backpack.add_item(GoldCoin(), 53)
    print('Backpack: worth -> {}, weight -> {}'.format(backpack.calculate_total_worth(), backpack.calculate_total_weight()))

