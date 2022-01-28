from abc import ABC, abstractstaticmethod
import slots

class BaseItem(ABC):
    def __init__(self, name=None, worth=0, weight=0, 
                slot=None, description='', sellable=True, **kwargs):
        if type(self) == BaseItem:
            raise NotImplementedError('Do not instantiate BaseItem directly')
        self.name = name
        self.worth = worth
        self.weight = weight
        self.slot = slot
        self.description = description
        self.sellable = sellable

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
            raise NotImplementedError('Do not instantiate Weapon directly')

class Rock(Weapon):
    def __init__(self, name='Rock', damage=5, worth=1, weight=1, 
                slot=slots.OneHand().name, **kwargs):
        super().__init__(name=name, damage=damage, worth=worth, weight=weight, 
                        slot=slot, **kwargs)

class Dagger(Weapon):
    def __init__(self, name='Dagger', damage=10, worth=20, weight=1, 
                slot=slots.OneHand().name, **kwargs):
        super().__init__(name=name, damage=damage, worth=worth, weight=weight,
                        slot=slot, **kwargs)

class Sword(Weapon):
    def __init__(self, name='Sword', damage=20, worth=100, weight=1, 
                slot=slots.OneHand().name, 
                description='Rusty', **kwargs):
        super().__init__(name=name, damage=damage, worth=worth, weight=weight, 
                        slot=slot, description=description, **kwargs)

class Crossbow(Weapon):
    def __init__(self, name='Crossbow', damage=15, worth=75, weight=2, 
                slot=slots.TwoHands(), **kwargs):
        super().__init__(name=name, damage=damage, worth=worth, weight=weight, 
                        slot=slot, **kwargs)

class Axe(Weapon):
    def __init__(self, name='Axe', damage=25, worth=60, weight=2, 
                slot=slots.TwoHands().name, **kwargs):
        super().__init__(name=name, damage=damage, worth=worth, weight=weight,
                        slot=slot, **kwargs)

# Consumables/Healing
class Consumable(BaseItem):
    def __init__(self, healing_value = 0, **kwargs):
        super().__init__(**kwargs)
        self.healing_value = healing_value
        if type(self) == Consumable:
            raise NotImplementedError('Do not instantiate Consumable directly')

    def __str__(self):
        return f'{self.description} {self.name} (+{self.healing_value})'

class Bread(Consumable):
    def __init__(self, name='Bread', healing_value=10, worth=12, weight=1,
                 slot=slots.SmallItem().name, description='Crusty', **kwargs):
        super().__init__(name=name, healing_value=healing_value, worth=worth, 
                        weight=weight, slot=slot, description=description, **kwargs)

class HealingPotion(Consumable):
    def __init__(self, name="Healing Potion", healing_value=50, worth=60,
                 weight=1, slot=slots.SmallItem().name, **kwargs):
        super().__init__(name=name, healing_value=healing_value, worth=worth, 
                        weight=weight, slot=slot, **kwargs)

# Containers
# class Container(BaseItem):
#     def __init__(self, update_limit=tuple(), **kwargs):
#         self.update_limit = update_limit
#         super().__init__(**kwargs)
#         if type(self) == Container:
#             raise NotImplementedError('Do not instantiate Container directly')
    
#     def updateSlotLimit(self, slots, amount=1, negative=False):
#         for slot in slots.__dict__.values():
#             # checks if self.update_limit is an emputy list
#             if not self.update_limit: return False
#             if not isinstance(slot, self.update_limit[0]): continue
#             if negative:
#                 slot.item_limit = slot.item_limit - self.update_limit[1] * amount
#                 return True
#             else:
#                 slot.item_limit = slot.item_limit + self.update_limit[1] * amount
#                 return True
        
# class Backpack(Container, BaseItem):
#     def __init__(self, name='Backpack', worth=10, weight=1, 
#                 slot=slots.Body().name, update_limit=(slots.SmallItem, 8), **kwargs):
#         super().__init__(name=name, worth=worth, weight=weight, 
#                         slot=slot, update_limit=update_limit, **kwargs)
    
# class CoinPouch(Container, BaseItem):
#     def __init__(self, name='Coin Pouch', worth=1, weight=.1, 
#                 slot=slots.SmallItem().name, update_limit=(slots.Coins, 50), **kwargs):
#         super().__init__(name=name, worth=worth, weight=weight, 
#                         slot=slot, update_limit=update_limit, **kwargs)

# Currency
class Coin(BaseItem):
    def __init__(self, worth=1, purity=1, slot=slots.Coins().name, sellable=False, **kwargs):
        super().__init__(weight=0.01, slot=slot, sellable=sellable, **kwargs)
        self.purity = purity
        self.worth = worth * purity
        if type(self) == Coin:
            raise NotImplementedError('Do not instantiate Coin directly')

class GreaterCoin(Coin):
    def __init__(self, **kwargs):
        super().__init__(purity=5, **kwargs)
        if type(self) == Coin:
            raise NotImplementedError('Do not instantiate GreaterCoin directly')

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

class GreaterPlatinumCoin(GreaterCoin, PlatinumCoin):
    def __init__(self, name='Greater Platinum Coin', **kwargs):
        super().__init__(name=name, **kwargs)


def main():
    # BaseItem()
    # Weapon()
    # Consumable()
    # Container()
    # Coin()
    print([CopperCoin(), Bread(), Sword()])
    # print(CopperCoin(), Dagger(), Bread(), Backpack(), Sword())
    
    c = CopperCoin()
    print(c.modifyAttr(name="l", ru=1))
    print(c.modifyAttr(name="small copper coin"))
    print(c.__dict__)

    # backpack = Backpack()
    # backpack.add_item(CopperCoin(), 10)
    # print('Backpack: worth -> {}, weight -> {}'.format(backpack.calculate_total_worth(), backpack.calculate_total_weight()))
    # backpack.add_item(GoldCoin(), 53)
    # print('Backpack: worth -> {}, weight -> {}'.format(backpack.calculate_total_worth(), backpack.calculate_total_weight()))
    # print(CoinPouch().slot)

if __name__ == "__main__":
    main()
