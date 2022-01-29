from abc import ABC
from dataclasses import dataclass
import setting

@dataclass(unsafe_hash=True)
class BaseItem(ABC):
    name: str = None
    worth: int = 0
    weight: int = 0
    slot: str = None
    description: str = None
    sellable: bool = True

    def __init__(self, *args, **kwargs):
        if type(self) == BaseItem:
            raise NotImplementedError('Do not instantiate BaseItem directly')

# Weapons
@dataclass(unsafe_hash=True)
class Weapon(BaseItem):
    damage: int = 0

    def __init__(self, *args, **kwargs):
        if type(self) == Weapon:
            raise NotImplementedError('Do not instantiate Weapon directly')

@dataclass(unsafe_hash=True)
class OneHandedWeapon(Weapon):
    slot: str = setting.ONE_HANDED_SLOT

    def __init__(self, *args, **kwargs):
        if type(self) == OneHandedWeapon:
            raise NotImplementedError('Do not instantiate OneHandedWeapon directly')

@dataclass(unsafe_hash=True)
class TwoHandedWeapon(Weapon):
    slot: str = setting.TWO_HANDED_SLOT

    def __init__(self, *args, **kwargs):
        if type(self) == TwoHandedWeapon:
            raise NotImplementedError('Do not instantiate TwoHandedWeapon directly')

@dataclass(unsafe_hash=True)
class Rock(OneHandedWeapon):
    name: str = 'Rock'
    worth: int = 1
    weight: int = 1
    damage: int = 5

@dataclass(unsafe_hash=True)
class Dagger(OneHandedWeapon):
    name: str = 'Dagger'
    worth: int = 1
    weight: int = 1
    damage: int = 5

@dataclass(unsafe_hash=True)
class Sword(OneHandedWeapon):
    name: str = 'Sword'
    worth: int = 1
    weight: int = 1
    damage: int = 5

@dataclass(unsafe_hash=True)
class Crossbow(TwoHandedWeapon):
    name: str = 'Crossbow'
    worth: int = 75
    weight: int = 2
    damage: int = 15

@dataclass(unsafe_hash=True)
class Axe(TwoHandedWeapon):
    name: str = 'Axe'
    worth: int = 60
    weight: int = 2
    damage: int = 25

# Consumables/Healing
@dataclass(unsafe_hash=True, init=False)
class Consumable(BaseItem):
    healing_value: int = 0
    slot: str = setting.MISC_SLOT

    def __init__(self, *args, **kwargs):
        if type(self) == Consumable:
            raise NotImplementedError('Do not instantiate Consumable directly')
    
    # def __str__(self):
    #     return f'{self.description} {self.name} (+{self.healing_value})'

@dataclass(unsafe_hash=True)
class Bread(Consumable):
    name: str = 'Bread'
    worth: int = 12
    weight: int = 1
    description: str = 'Cursty'
    healing_value: int = 10

@dataclass(unsafe_hash=True)
class HealingPotion(Consumable):
    name: str = 'Healing Potion'
    worth: int = 60
    weight: int = 1
    healing_value: int = 50


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
@dataclass(unsafe_hash=True)
class Coin(BaseItem):
    purity: int = 1
    weight: int = 0.01
    slot: str = setting.COIN_SLOT
    sellable: bool = False

    def __init__(self, *args, **kwargs):
        self.worth = self.worth * self.purity
        if type(self) == Coin:
            raise NotImplementedError('Do not instantiate Coin directly')

@dataclass(unsafe_hash=True)
class GreaterCoin(Coin):
    purity: int = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if type(self) == Coin:
            raise NotImplementedError('Do not instantiate GreaterCoin directly')

@dataclass(unsafe_hash=True)
class CopperCoin(Coin):
    name: str = 'Copper Coin'
    worth: int = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

@dataclass(unsafe_hash=True)
class GreaterCopperCoin(GreaterCoin, CopperCoin):
    name: str = 'Greater Copper Coin'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

@dataclass(unsafe_hash=True)
class SilverCoin(Coin):
    name: str = 'Silver Coin'
    worth: int = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

@dataclass(unsafe_hash=True)
class GreaterSilverCoin(GreaterCoin, SilverCoin):
    name: str = 'Greater Silver Coin'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

@dataclass(unsafe_hash=True)
class GoldCoin(Coin):
    name: str = 'Gold Coin'
    worth: int = 100

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

@dataclass(unsafe_hash=True)
class GreaterGoldCoin(GreaterCoin, GoldCoin):
    name: str = 'Greater Gold Coin'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

@dataclass(unsafe_hash=True)
class PlatinumCoin(Coin):
    name: str = 'Platinum Coin'
    worth: int = 100

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

@dataclass(unsafe_hash=True)
class GreaterPlatinumCoin(GreaterCoin, PlatinumCoin):
    name: str = 'Greater Platinum Coin'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)




def main():
    # BaseItem()
    # Weapon()
    # Consumable()
    # Container()
    c = GoldCoin()
    gc = GreaterSilverCoin()
    b = Bread()
    print(b)
    print(c, gc)
    print(f'{b}')
    
    # print([CopperCoin(), Bread(), Sword()])
    # # print(CopperCoin(), Dagger(), Bread(), Backpack(), Sword())
    
    # c = CopperCoin()
    # print(c.modifyAttr(name="l", ru=1))
    # print(c.modifyAttr(name="small copper coin"))
    # print(c.__dict__)

    # backpack = Backpack()
    # backpack.add_item(CopperCoin(), 10)
    # print('Backpack: worth -> {}, weight -> {}'.format(backpack.calculate_total_worth(), backpack.calculate_total_weight()))
    # backpack.add_item(GoldCoin(), 53)
    # print('Backpack: worth -> {}, weight -> {}'.format(backpack.calculate_total_worth(), backpack.calculate_total_weight()))
    # print(CoinPouch().slot)


if __name__ == "__main__":
    main()
