from abc import ABC
from dataclasses import dataclass
from container import Container
from items import BaseItem
import setting



@dataclass()
class Slot(Container):
    type: str = None
    item_limit: int = None
    
    def addItem(self, item: BaseItem, amount: int=1) -> bool:
        # Checks if there a limit or not
        if self.item_limit:
            # Check if limit was passed
            if len(self.container) >= self.item_limit: 
                return False
        # Adds another items if exist
        if item in self.container:
            self.container[item]['amount'] += amount
            return True
        # Adds new item
        else:
            self.container[item] = {'amount': amount}
            return True

@dataclass()
class Head(Slot):
    type: str = setting.HEAD_SLOT
    item_limit: int = 1

@dataclass()
class Body(Slot):
    type: str = setting.BODY_SLOT
    item_limit: int = 1

@dataclass()
class Legs(Slot):
    type: str = setting.LEGS_SLOT
    item_limit: int = 1

@dataclass()
class OneHanded(Slot):
    type: str = setting.ONE_HANDED_SLOT
    item_limit: int = 1
    
@dataclass()    
class TwoHanded(Slot):
    type: str = setting.TWO_HANDED_SLOT
    item_limit: int = 1

@dataclass()
class Coins(Slot):
    type: str = setting.COIN_SLOT

    def order(self) -> list:
        # Puts the container from largest worth to smallest
        coins = list(self.container.items())
        worth = lambda coin: coin[0].worth
        coins.sort(key=worth)  # Sort function only works with a list type
        ordict = dict(coins)
        self.container.clear()
        self.container.update(ordict)

@dataclass()
class Miscellaneous(Slot):
    type: str = setting.MISC_SLOT


def main():
    import items
    a = OneHanded()
    b = OneHanded()
    c = TwoHanded()
    print(a==b)
    print(a is b)
    print(a.container==b.container)
    print(a.container is b.container)

    print('_'*20)
    print(a == c)
    print(a is c , "here")
    print(a.container==c.container)
    print(a.container is c.container)






if __name__ == "__main__":
    main()
