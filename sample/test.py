from abc import ABC, abstractstaticmethod
from dataclasses import dataclass
import setting


ONE_HANDED_SLOT = 'One Handed'

# class BaseItem(ABC):
#     def __init__(self, name=None, worth=0, weight=0, 
#                 slot=None, description='', **kwargs):
#         if type(self) == BaseItem:
#             raise Exception('Do not instantiate BaseItem directly')
#         self.name = name
#         self.worth = worth
#         self.weight = weight
#         self.slot = slot
#         self.description = description

#     # def __str__(self):
#     #     if self.description:
#     #         return f'{self.description} {self.name}'
#     #     else:
#     #         return f'{self.name}'

#     # def __repr__(self):
#     #     return f'{self.__class__.__name__}()'

# # Weapons
# class Weapon(BaseItem):
#     def __init__(self, damage = 0, **kwargs):
#         super().__init__(**kwargs)
#         self.damage = damage
#         if type(self) == Weapon:
#             raise Exception('Do not instantiate Weapon directly')

# class Rock(Weapon):
#     def __init__(self, name='Rock', damage=5, worth=1, weight=1, 
#                 slot=ONE_HANDED_SLOT, **kwargs):
#         super().__init__(name=name, damage=damage, worth=worth, weight=weight, 
#                         slot=slot, **kwargs)





@dataclass(frozen=True)
class BaseItem(ABC):
    name: str
    _worth: int
    weight: int = 0
    slot: str = None
    description: str = None
    sellable: bool = True

    def __post_init__(self):
        self.worth = self._worth

    # def __init__(self, *args, **kwargs):
    #     if type(self) == BaseItem:
    #         raise NotImplementedError('Do not instantiate BaseItem directly')

# Weapons
@dataclass(frozen=True)
class Weapon(BaseItem):
    damage: int = 0

    def __init__(self, *args, **kwargs):
        if type(self) == Weapon:
            raise NotImplementedError('Do not instantiate Weapon directly')

@dataclass(frozen=True)
class OneHandedWeapon(Weapon):
    slot: str = ONE_HANDED_SLOT

    def __init__(self, *args, **kwargs):
        if type(self) == OneHandedWeapon:
            raise NotImplementedError('Do not instantiate OneHandedWeapon directly')


@dataclass(frozen=True)
class Rock2(Weapon):
    name: str = 'Rock'
    _worth: int = 1
    weight: int = 1
    damage: int = 5


@dataclass(frozen=True)
class Coin(BaseItem):
    purity: int = 1
    weight: int = 0.01
    slot: str = setting.COIN_SLOT
    sellable: bool = False

    # def __init__(self, *args, **kwargs):
    #     self.worth = self.worth * self.purity
    #     if type(self) == Coin:
    #         raise NotImplementedError('Do not instantiate Coin directly')


@dataclass(frozen=True)
class GreaterCoin(Coin):
    purity: int = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if type(self) == Coin:
            raise NotImplementedError('Do not instantiate GreaterCoin directly')


@dataclass(frozen=True)
class CopperCoin(Coin):
    name: str = 'Copper Coin'
    _worth: int = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# def main():
#     a = Rock()
#     b = Rock()
#     c = Rock()

#     print(a, b, c)
#     print(a==b, b==c, a==c)
#     print(a is b, b is c, a is c)

def main2():
    a = Rock2()
    b = Rock2()
    c = Rock2()
    C = CopperCoin()

    print(C)
    # print(a, b, c)
    # print(a==b, b==c, a==c)
    # print(a is b, b is c, a is c)


if __name__ == "__main__":
    # main()
    main2()
