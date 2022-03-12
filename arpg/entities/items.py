# Standard library imports  
from dataclasses import dataclass
from typing import Optional
from abc import ABC

# Local application imports
import entities.slots as slots



@dataclass(frozen=True)
class BaseItem(ABC):
    name: str = ''
    worth: int = 0
    weight: int = 0
    slot_type: slots.Slot = slots.Miscellaneous
    description: Optional[str] = None

    def __init__(self, *args, **kwargs):
        if type(self) == BaseItem:
            raise NotImplementedError('Do not instantiate BaseItem directly')


# Weapons
@dataclass(frozen=True)
class Weapon(BaseItem):
    damage: int = 0

    def __init__(self, *args, **kwargs):
        if type(self) == Weapon:
            raise NotImplementedError('Do not instantiate Weapon directly')


# One Handed Weapons
@dataclass(frozen=True)
class OneHandedWeapon(Weapon):
    slot_type: slots.Slot = slots.OneHanded

    def __init__(self, *args, **kwargs):
        if type(self) == OneHandedWeapon:
            raise NotImplementedError('Do not instantiate OneHandedWeapon directly')

@dataclass(frozen=True)
class Rock(OneHandedWeapon):
    name: str = 'Rock'
    worth: int = 1
    weight: int = 1
    damage: int = 5

@dataclass(frozen=True)
class Dagger(OneHandedWeapon):
    name: str = 'Dagger'
    worth: int = 200
    weight: int = 1
    damage: int = 5

@dataclass(frozen=True)
class Sword(OneHandedWeapon):
    name: str = 'Sword'
    worth: int = 500
    weight: int = 1
    damage: int = 5


# Two Handed Weapons
@dataclass(frozen=True)
class TwoHandedWeapon(Weapon):
    slot_type: slots.Slot = slots.TwoHanded

    def __init__(self, *args, **kwargs):
        if type(self) == TwoHandedWeapon:
            raise NotImplementedError('Do not instantiate TwoHandedWeapon directly')

@dataclass(frozen=True)
class Crossbow(TwoHandedWeapon):
    name: str = 'Crossbow'
    worth: int = 750
    weight: int = 2
    damage: int = 15

@dataclass(frozen=True)
class Axe(TwoHandedWeapon):
    name: str = 'Axe'
    worth: int = 600
    weight: int = 2
    damage: int = 25


# Consumables/Healing
@dataclass(frozen=True)
class Consumable(BaseItem):
    healing_value: int = 0

    def __init__(self, *args, **kwargs):
        if type(self) == Consumable:
            raise NotImplementedError('Do not instantiate Consumable directly')

@dataclass(frozen=True)
class Bread(Consumable):
    name: str = 'Bread'
    worth: int = 12
    weight: int = 1
    description: str = 'Cursty'
    healing_value: int = 10

@dataclass(frozen=True)
class HealingPotion(Consumable):
    name: str = 'Healing Potion'
    worth: int = 600
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
#         for slot_type in slots.__dict__.values():
#             # checks if self.update_limit is an emputy list
#             if not self.update_limit: return False
#             if not isinstance(slot_type, self.update_limit[0]): continue
#             if negative:
#                 slot_type.item_limit = slot_type.item_limit - self.update_limit[1] * amount
#                 return True
#             else:
#                 slot_type.item_limit = slot_type.item_limit + self.update_limit[1] * amount
#                 return True
        
# class Backpack(Container, BaseItem):
#     def __init__(self, name='Backpack', worth=10, weight=1, 
#                 slot_type=slots.Body().name, update_limit=(slots.SmallItem, 8), **kwargs):
#         super().__init__(name=name, worth=worth, weight=weight, 
#                         slot_type=slot_type, update_limit=update_limit, **kwargs)
    
# class CoinPouch(Container, BaseItem):
#     def __init__(self, name='Coin Pouch', worth=1, weight=.1, 
#                 slot_type=slots.SmallItem().name, update_limit=(slots.Coins, 50), **kwargs):
#         super().__init__(name=name, worth=worth, weight=weight, 
#                         slot_type=slot_type, update_limit=update_limit, **kwargs)

